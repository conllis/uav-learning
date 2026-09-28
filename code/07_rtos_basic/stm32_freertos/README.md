# STM32 + FreeRTOS 最小任务骨架

对应仓库提交 `6ab3ad21b1d26c093fa3a7defcc197a2a19d1d50` 的
`freertos_task_sim.py`。这是供 STM32CubeMX/CubeIDE 工程复制的应用层源码；
尚未指定 STM32 型号和开发板，因此不含 `.ioc`、启动文件、HAL 或真实驱动。
默认以确定性的虚拟 IMU 信号运行，四路电机值只在 RAM 中预览。

## 文件及数据流

```text
Core/Inc/uav_rtos_app.h       数据类型、快照及启动 API
Core/Inc/uav_board_port.h     板级接口
Core/Src/uav_rtos_app.c       六个 FreeRTOS 任务与超时保护
Core/Src/uav_board_port.c     虚拟 IMU、LED/遥测占位接口

UavBoard_ReadImu → [IMU Queue, 1 item] → attitude_task
              → [Attitude Queue, 1 item] → control_task → RAM preview
                                 │
                   Mutex-protected shared snapshot
                                 │
                      safety / telemetry / debugger
```

长度为 1 的队列用 `xQueueOverwrite` 保留最新值；任务在自己的周期点以
`xQueueReceive(..., 0)` 取样。队列自身已同步，只有跨任务读取的快照使用
`xSemaphoreCreateMutex`。板级遥测调用放在 Mutex 外。

| 任务 | 周期 | 频率 | 优先级 |
| --- | ---: | ---: | ---: |
| safety | 50 ms | 20 Hz | 6 |
| IMU | 5 ms | 200 Hz | 5 |
| attitude | 5 ms | 200 Hz | 4 |
| control | 10 ms | 100 Hz | 3 |
| telemetry | 100 ms | 10 Hz | 2 |
| heartbeat | 1000 ms | 1 Hz | 1 |

所有任务在每轮末尾调用 `vTaskDelayUntil`。优先级数越大越先调度。
在同一个 5 ms 边界，IMU 先写入，再由姿态读取；控制每 10 ms 取一次最新姿态。

## 移植步骤

1. 在 STM32CubeMX 选择实际芯片/开发板，启用 FreeRTOS、GPIO LED、调试接口；
   首次不必启用 SPI/I2C/PWM。生成 CubeIDE 工程，先编译 CubeMX 原始工程。
2. 设置 FreeRTOS `configTICK_RATE_HZ = 1000`、`configMAX_PRIORITIES >= 7`、
   `configUSE_PREEMPTION = 1`、`configUSE_MUTEXES = 1`、
   `INCLUDE_vTaskDelayUntil = 1`。在 CubeMX 的任务/堆设置中留出六个
   任务栈、两个队列和一个 Mutex 的空间；任务创建失败须停止启动并排查堆。
   栈深度 `xTaskCreate` 的 192/256/384 是 FreeRTOS **StackType_t 字数**，
   通常在 Cortex-M 上一字为 4 字节，移植后按栈高水位调整。
3. 将本目录的四个 `.h/.c` 复制到 CubeMX 工程对应的 `Core/Inc`、
   `Core/Src`，加入编译源文件，并使编译器能找到 FreeRTOS 头文件；
   浮点三角函数需要链接数学库 `-lm`（CubeIDE 工程如已有则不重复设置）。
4. 在生成的 `freertos.c` 中、`MX_FREERTOS_Init(void)` 的
   `USER CODE BEGIN/END` 区域调用：

   ```c
   #include "uav_rtos_app.h"  /* 放到 USER CODE Includes */

   /* 放到 MX_FREERTOS_Init 的 USER CODE 区域；调用只执行一次 */
   if (UavRtos_Start() != pdPASS) {
       Error_Handler();
   }
   ```

   使用原生 FreeRTOS API 创建任务；`MX_FREERTOS_Init` 应在调度器启动前执行。
   如 CubeMX 已建默认任务，它会额外占堆和 CPU，可删除无用默认任务。
   CubeMX 再生成代码时只保留 USER CODE 区域，必要时核对调用是否仍在。
5. 首次在调试器中查看 `UavRtos_GetSnapshot(&snapshot)` 返回的计数与姿态。
   LED 和 UART 当前为空实现；按开发板改写 `uav_board_port.c` 中的
   `UavBoard_Heartbeat`、`UavBoard_Telemetry`。遥测用 DMA/环形缓冲优先；
   若暂用阻塞 UART，应限定其时间，且始终在 Mutex 外调用。
6. 替换 `UavBoard_ReadImu` 为实际传感器读取：`ax/ay/az` 单位 g，
   `gx/gy/gz` 单位 deg/s。采样应有明确时间戳；目前任务在读完后用 RTOS
   tick 标时。若改为 DMA/中断采样，应传递**采样时刻**且处理总线超时、
   数据重复和溢出；不要把传感器的原始微秒时间直接当 RTOS tick。
7. 最后才考虑输出驱动。当前 `preview` 是仿真控制量，**未做解锁、
   姿态限幅、传感器标定或实际飞行安全验证，不应接电机**。故障锁存后
   `preview` 归零；复位 MCU 才解除锁存，避免故障刚恢复时自动输出。

## 超时和观察点

- IMU 超过 100 ms 无有效数据，或控制超过 200 ms 未处理有效新姿态，
  安全任务锁存 `fault_latched`；启动时分别给这两个期限作为宽限期。
- 控制只接受本轮队列中新姿态，且其 IMU 样本年龄不超过 20 ms；
  没有新数据则 `preview` 当轮归零，不重复使用过期姿态。
- `safety_ok` 初始为 false；收到 IMU 和有效控制结果后，
  安全任务下一轮才将它置 true。安全任务检测按 50 ms 周期，
  故障识别有至多约一个检查周期的额外延迟。
- 正常运行约 8 秒时，六个计数分别接近 1600、1600、800、
  160、80、8（启动边界可能多 1）。可断点/观察 `UavSnapshot`。
  人工令 `UavBoard_ReadImu` 持续返回 false：最多约 150 ms 后
  `fault_latched` 置 true，控制预览保持零。恢复数据不会自动解锁。
- 高优先级任务应在其周期内完成；如果 `vTaskDelayUntil` 发现预定
  唤醒时刻已过去，它不会等待，会连续赶周期。实板应测执行时间和栈余量，
  修正负载、优先级与外设阻塞调用。

说明：Python 仿真运行 8 秒后写 CSV；嵌入式任务一直运行，低频遥测接口和
调试快照替代 CSV。这里用互补滤波和比例控制保留原演示算法，尚非飞控方案。
