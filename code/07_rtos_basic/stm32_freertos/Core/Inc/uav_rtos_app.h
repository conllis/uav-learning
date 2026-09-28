#ifndef UAV_RTOS_APP_H
#define UAV_RTOS_APP_H

#include <stdbool.h>
#include <stdint.h>
#include "FreeRTOS.h"
#include "task.h"

typedef struct {
    float ax, ay, az;             /* acceleration in g */
    float gx, gy, gz;             /* angular rate in deg/s */
    TickType_t sample_tick;
} UavImu;

typedef struct {
    float roll, pitch, yaw;       /* degrees */
    TickType_t sample_tick;       /* originating IMU sample */
} UavAttitude;

typedef struct {
    float motor1, motor2, motor3, motor4; /* preview only, range 0..1 */
    TickType_t update_tick;
} UavMotorPreview;

typedef struct {
    UavImu imu;
    UavAttitude attitude;
    UavMotorPreview preview;
    uint32_t imu_count, attitude_count, control_count;
    uint32_t safety_count, telemetry_count, heartbeat_count;
    TickType_t last_imu_tick, last_control_tick;
    bool has_imu, has_attitude, has_control;
    bool safety_ok, fault_latched;
} UavSnapshot;

/* Call once in MX_FREERTOS_Init(), before osKernelStart(). */
BaseType_t UavRtos_Start(void);
/* A bounded snapshot for debugger, telemetry, or future board adapters. */
bool UavRtos_GetSnapshot(UavSnapshot *out);

#endif
