#ifndef UAV_BOARD_PORT_H
#define UAV_BOARD_PORT_H

#include "uav_rtos_app.h"

/* Replace the synthetic reader with an actual IMU driver during hardware porting. */
bool UavBoard_ReadImu(UavImu *out);
void UavBoard_Heartbeat(bool led_on);
void UavBoard_Telemetry(const UavSnapshot *snapshot);

#endif
