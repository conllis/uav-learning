# Day 84 STM32 + FreeRTOS 小系统设计

## 1. 今日目标

理解如何把一个小型飞控系统拆分成多个 FreeRTOS 任务，明确 IMU 采样、姿态解算、控制输出、遥测通信和安全检查之间的关系。

---

## 2. 为什么需要 FreeRTOS

裸机程序通常是：

```c
while (1)
{
    read_imu();
    update_attitude();
    control_motor();
    send_uart();
    blink_led();
}

问题：

所有功能混在一起
某个函数卡住会影响整个系统
不同频率任务不好管理
后期扩展困难

FreeRTOS 可以把系统拆成多个任务，让不同任务按优先级和周期运行。

3. FreeRTOS 核心概念
Task

Task 是一个独立运行的任务，例如：

IMU 采样任务
姿态解算任务
控制任务
通信任务
LED 心跳任务
Priority

Priority 是任务优先级。

和飞行安全直接相关的任务优先级应该更高。

Queue

Queue 用于任务之间传递数据。

例如：

imu_task -> imu_queue -> attitude_task
Semaphore

Semaphore 可以用于任务通知，例如传感器数据准备好后通知处理任务。

Mutex

Mutex 用于保护共享资源，例如 UART 打印。

4. 小飞控任务设计
任务	作用	频率	优先级
imu_task	读取 IMU	200Hz / 500Hz	高
attitude_task	姿态解算	200Hz	高
control_task	姿态控制和电机输出	100Hz / 200Hz	高
telemetry_task	串口输出调试信息	10Hz	中
safety_task	异常检测和保护	20Hz	高
heartbeat_task	LED 心跳灯	1Hz	低
5. 系统数据流
IMU
  ↓
imu_task
  ↓
imu_queue
  ↓
attitude_task
  ↓
attitude_queue
  ↓
control_task
  ↓
motor_output

辅助任务：

telemetry_task：输出调试信息
heartbeat_task：LED 闪烁
safety_task：检查异常
6. 数据结构设计
IMU 数据
typedef struct
{
    float ax;
    float ay;
    float az;

    float gx;
    float gy;
    float gz;

    uint32_t timestamp_ms;
} imu_data_t;
姿态数据
typedef struct
{
    float roll;
    float pitch;
    float yaw;

    uint32_t timestamp_ms;
} attitude_data_t;
电机输出
typedef struct
{
    float motor1;
    float motor2;
    float motor3;
    float motor4;
} motor_output_t;
7. 任务伪代码
void imu_task(void *argument)
{
    TickType_t last_wake_time = xTaskGetTickCount();

    while (1)
    {
        read_imu();
        send_imu_data_to_queue();

        vTaskDelayUntil(&last_wake_time, pdMS_TO_TICKS(5));
    }
}
void attitude_task(void *argument)
{
    while (1)
    {
        if (xQueueReceive(imu_queue, &imu, portMAX_DELAY) == pdPASS)
        {
            estimate_attitude();
            send_attitude_to_queue();
        }
    }
}
void control_task(void *argument)
{
    TickType_t last_wake_time = xTaskGetTickCount();

    while (1)
    {
        receive_attitude();
        run_pid();
        update_motor_pwm();

        vTaskDelayUntil(&last_wake_time, pdMS_TO_TICKS(5));
    }
}
8. 设计原则
高频任务不要做耗时操作。
UART 打印不要放在 IMU 高频任务里。
控制任务和 IMU 任务优先级要高。
LED、调试输出优先级可以低。
任务之间尽量用 Queue 或 Semaphore 通信。
共享资源要用 Mutex 保护。
周期任务优先使用 vTaskDelayUntil()。
9. 和无人机系统的关系

在真实飞控中：

IMU 任务提供原始传感器数据
姿态解算任务估计 roll / pitch / yaw
控制任务根据目标姿态和当前姿态计算电机输出
通信任务负责遥测和调参
安全任务负责异常保护

这和 PX4 内部结构类似，只是 PX4 更复杂。

10. 今日总结

STM32 + FreeRTOS 小系统的核心不是“多写几个 while 循环”，而是把不同频率、不同重要程度的功能拆成任务。

一句话总结：

FreeRTOS 让 STM32 程序从“单线程轮流执行”变成“多任务按优先级协作执行”。
