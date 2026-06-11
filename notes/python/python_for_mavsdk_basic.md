# Python for MAVSDK 基础知识

## 1. Python 在本项目中的作用

Python 用来通过 MAVSDK 连接 PX4 SITL，读取 telemetry，并发送 Action 命令。

## 2. 必须掌握的知识

- import
- 变量
- float / bool / str / dict / list
- def
- async def
- await
- async for
- if
- try / except
- f-string
- CSV 文件写入
- pandas 读取 CSV
- matplotlib 画图
- asyncio.create_task

## 3. 最重要的理解

Telemetry 是持续数据流，所以 MAVSDK Python 使用 async / await。

Action 是异步命令，所以 arm、takeoff、land 都需要 await。

Action 发命令，Telemetry 看结果。
