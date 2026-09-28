#include "uav_rtos_app.h"
#include "uav_board_port.h"

#include <math.h>
#include <string.h>
#include "queue.h"
#include "semphr.h"

/* 1 ms tick makes 5/10/50/100/1000 ms exact integer periods. */
#if configTICK_RATE_HZ != 1000
#error "This example requires configTICK_RATE_HZ == 1000"
#endif
#if configMAX_PRIORITIES < 7
#error "This example requires configMAX_PRIORITIES >= 7"
#endif

#define IMU_PERIOD        pdMS_TO_TICKS(5)
#define ATTITUDE_PERIOD   pdMS_TO_TICKS(5)
#define CONTROL_PERIOD    pdMS_TO_TICKS(10)
#define SAFETY_PERIOD     pdMS_TO_TICKS(50)
#define TELEMETRY_PERIOD  pdMS_TO_TICKS(100)
#define HEARTBEAT_PERIOD  pdMS_TO_TICKS(1000)
#define IMU_TIMEOUT       pdMS_TO_TICKS(100)
#define CONTROL_TIMEOUT   pdMS_TO_TICKS(200)
#define DATA_MAX_AGE      pdMS_TO_TICKS(20)
#define STATE_WAIT        pdMS_TO_TICKS(1)
#define DEG_PER_RAD       57.2957795f

static QueueHandle_t s_imu_queue;
static QueueHandle_t s_attitude_queue;
static SemaphoreHandle_t s_state_mutex;
static UavSnapshot s_state;
static TickType_t s_start_tick;

bool UavRtos_GetSnapshot(UavSnapshot *out)
{
    if ((out == NULL) || (s_state_mutex == NULL) ||
        (xSemaphoreTake(s_state_mutex, STATE_WAIT) != pdTRUE)) {
        return false;
    }
    *out = s_state;
    (void)xSemaphoreGive(s_state_mutex);
    return true;
}

static bool imu_valid(const UavImu *v)
{
    return isfinite(v->ax) && isfinite(v->ay) && isfinite(v->az) &&
           isfinite(v->gx) && isfinite(v->gy) && isfinite(v->gz);
}

static void imu_task(void *argument)
{
    (void)argument;
    TickType_t wake = xTaskGetTickCount();
    for (;;) {
        UavImu imu;
        if (UavBoard_ReadImu(&imu) && imu_valid(&imu)) {
            imu.sample_tick = xTaskGetTickCount();
            (void)xQueueOverwrite(s_imu_queue, &imu);
            if (xSemaphoreTake(s_state_mutex, STATE_WAIT) == pdTRUE) {
                s_state.imu = imu;
                s_state.last_imu_tick = imu.sample_tick;
                s_state.has_imu = true;
                s_state.imu_count++;
                (void)xSemaphoreGive(s_state_mutex);
            }
        }
        vTaskDelayUntil(&wake, IMU_PERIOD);
    }
}

static void attitude_task(void *argument)
{
    (void)argument;
    TickType_t wake = xTaskGetTickCount();
    TickType_t previous_sample = 0;
    bool have_previous = false;
    float roll = 0.0f, pitch = 0.0f, yaw = 0.0f;
    for (;;) {
        UavImu imu;
        if (xQueueReceive(s_imu_queue, &imu, 0) == pdTRUE) {
            const TickType_t elapsed = imu.sample_tick - previous_sample;
            const float dt = (have_previous && elapsed > 0 &&
                              elapsed <= pdMS_TO_TICKS(50))
                           ? (float)elapsed / 1000.0f : 0.005f;
            previous_sample = imu.sample_tick;
            have_previous = true;
            const float accel_roll = atan2f(imu.ay, imu.az) * DEG_PER_RAD;
            const float accel_pitch = atan2f(-imu.ax,
                                             sqrtf(imu.ay * imu.ay + imu.az * imu.az))
                                      * DEG_PER_RAD;
            roll = 0.98f * (roll + imu.gx * dt) + 0.02f * accel_roll;
            pitch = 0.98f * (pitch + imu.gy * dt) + 0.02f * accel_pitch;
            yaw += imu.gz * dt;
            const UavAttitude attitude = {roll, pitch, yaw, imu.sample_tick};
            (void)xQueueOverwrite(s_attitude_queue, &attitude);
            if (xSemaphoreTake(s_state_mutex, STATE_WAIT) == pdTRUE) {
                s_state.attitude = attitude;
                s_state.has_attitude = true;
                s_state.attitude_count++;
                (void)xSemaphoreGive(s_state_mutex);
            }
        }
        vTaskDelayUntil(&wake, ATTITUDE_PERIOD);
    }
}

static float clamp01(float v)
{
    return fminf(1.0f, fmaxf(0.0f, v));
}

static void control_task(void *argument)
{
    (void)argument;
    TickType_t wake = xTaskGetTickCount();
    for (;;) {
        UavAttitude attitude;
        const TickType_t now = xTaskGetTickCount();
        const bool fresh = (xQueueReceive(s_attitude_queue, &attitude, 0) == pdTRUE) &&
                           ((TickType_t)(now - attitude.sample_tick) <= DATA_MAX_AGE);
        if (xSemaphoreTake(s_state_mutex, STATE_WAIT) == pdTRUE) {
            /* Neutral on missing/stale input; never invoke a real motor driver. */
            memset(&s_state.preview, 0, sizeof(s_state.preview));
            s_state.preview.update_tick = now;
            if (fresh && !s_state.fault_latched) {
                const float r = -0.01f * attitude.roll;
                const float p = -0.01f * attitude.pitch;
                s_state.preview.motor1 = clamp01(0.5f + r + p);
                s_state.preview.motor2 = clamp01(0.5f - r + p);
                s_state.preview.motor3 = clamp01(0.5f - r - p);
                s_state.preview.motor4 = clamp01(0.5f + r - p);
                s_state.last_control_tick = now;
                s_state.has_control = true;
                s_state.control_count++;
            }
            (void)xSemaphoreGive(s_state_mutex);
        }
        vTaskDelayUntil(&wake, CONTROL_PERIOD);
    }
}

static void safety_task(void *argument)
{
    (void)argument;
    TickType_t wake = xTaskGetTickCount();
    for (;;) {
        const TickType_t now = xTaskGetTickCount();
        if (xSemaphoreTake(s_state_mutex, STATE_WAIT) == pdTRUE) {
            const bool imu_timeout = s_state.has_imu
                ? (TickType_t)(now - s_state.last_imu_tick) > IMU_TIMEOUT
                : (TickType_t)(now - s_start_tick) > IMU_TIMEOUT;
            const bool control_timeout = s_state.has_control
                ? (TickType_t)(now - s_state.last_control_tick) > CONTROL_TIMEOUT
                : (TickType_t)(now - s_start_tick) > CONTROL_TIMEOUT;
            if (imu_timeout || control_timeout) {
                s_state.fault_latched = true;
                memset(&s_state.preview, 0, sizeof(s_state.preview));
                s_state.preview.update_tick = now;
            }
            s_state.safety_ok = s_state.has_imu && s_state.has_control &&
                                !s_state.fault_latched;
            s_state.safety_count++;
            (void)xSemaphoreGive(s_state_mutex);
        }
        vTaskDelayUntil(&wake, SAFETY_PERIOD);
    }
}

static void telemetry_task(void *argument)
{
    (void)argument;
    TickType_t wake = xTaskGetTickCount();
    for (;;) {
        UavSnapshot snapshot;
        if (xSemaphoreTake(s_state_mutex, STATE_WAIT) == pdTRUE) {
            s_state.telemetry_count++;
            snapshot = s_state;
            (void)xSemaphoreGive(s_state_mutex);
            UavBoard_Telemetry(&snapshot); /* Outside mutex: UART must not block control. */
        }
        vTaskDelayUntil(&wake, TELEMETRY_PERIOD);
    }
}

static void heartbeat_task(void *argument)
{
    (void)argument;
    TickType_t wake = xTaskGetTickCount();
    bool led_on = false;
    for (;;) {
        led_on = !led_on;
        UavBoard_Heartbeat(led_on);
        if (xSemaphoreTake(s_state_mutex, STATE_WAIT) == pdTRUE) {
            s_state.heartbeat_count++;
            (void)xSemaphoreGive(s_state_mutex);
        }
        vTaskDelayUntil(&wake, HEARTBEAT_PERIOD);
    }
}

BaseType_t UavRtos_Start(void)
{
    s_start_tick = xTaskGetTickCount();
    memset(&s_state, 0, sizeof(s_state));
    s_imu_queue = xQueueCreate(1, sizeof(UavImu));
    s_attitude_queue = xQueueCreate(1, sizeof(UavAttitude));
    s_state_mutex = xSemaphoreCreateMutex();
    if (!s_imu_queue || !s_attitude_queue || !s_state_mutex) {
        return pdFAIL;
    }
    /* Priorities: safety 6 > IMU 5 > attitude 4 > control 3 > telemetry 2 > LED 1. */
    if (xTaskCreate(safety_task, "safety", 256, NULL, 6, NULL) != pdPASS ||
        xTaskCreate(imu_task, "imu", 256, NULL, 5, NULL) != pdPASS ||
        xTaskCreate(attitude_task, "attitude", 384, NULL, 4, NULL) != pdPASS ||
        xTaskCreate(control_task, "control", 256, NULL, 3, NULL) != pdPASS ||
        xTaskCreate(telemetry_task, "telemetry", 256, NULL, 2, NULL) != pdPASS ||
        xTaskCreate(heartbeat_task, "heartbeat", 192, NULL, 1, NULL) != pdPASS) {
        return pdFAIL; /* Fail startup: do not start the scheduler on partial creation. */
    }
    return pdPASS;
}
