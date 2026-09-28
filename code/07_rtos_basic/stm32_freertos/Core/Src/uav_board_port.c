#include "uav_board_port.h"

#include <math.h>

/* Deterministic input for the first board bring-up. No I2C/SPI or motors. */
bool UavBoard_ReadImu(UavImu *out)
{
    if (out == NULL) {
        return false;
    }
    const float t = (float)xTaskGetTickCount() / (float)configTICK_RATE_HZ;
    const float roll = (10.0f * sinf(2.0f * 3.14159265f * 0.25f * t)) * 0.01745329252f;
    const float pitch = (5.0f * sinf(2.0f * 3.14159265f * 0.20f * t)) * 0.01745329252f;
    out->ax = -sinf(pitch);
    out->ay = sinf(roll) * cosf(pitch);
    out->az = cosf(roll) * cosf(pitch);
    out->gx = 15.0f * cosf(2.0f * 3.14159265f * 0.25f * t);
    out->gy = 6.0f * cosf(2.0f * 3.14159265f * 0.20f * t);
    out->gz = 2.0f;
    out->sample_tick = xTaskGetTickCount();
    return true;
}

void UavBoard_Heartbeat(bool led_on)
{
    (void)led_on; /* Map to HAL_GPIO_WritePin for the chosen board. */
}

void UavBoard_Telemetry(const UavSnapshot *snapshot)
{
    (void)snapshot; /* Map to DMA/UART or inspect UavRtos_GetSnapshot in debugger. */
}
