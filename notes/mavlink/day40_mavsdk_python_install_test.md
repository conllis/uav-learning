# Day 40 安装并测试 MAVSDK Python

## 今日目标

今天安装 MAVSDK Python，并编写一个最小连接测试程序，确认 Python 程序能够连接 PX4 SITL。

---

## 1. 项目目录

本次项目目录：

```text
~/uav-learning/code/03_mavsdk_telemetry
```

创建命令：

```bash
cd ~/uav-learning
mkdir -p code/03_mavsdk_telemetry
cd code/03_mavsdk_telemetry
```

---

## 2. 创建 Python 虚拟环境

创建虚拟环境：

```bash
python3 -m venv venv
```

激活虚拟环境：

```bash
source venv/bin/activate
```

如果缺少 venv 模块，可以安装：

```bash
sudo apt update
sudo apt install python3-venv -y
```

---

## 3. 安装 MAVSDK Python

在虚拟环境中安装：

```bash
pip install --upgrade pip
pip install mavsdk
```

检查安装是否成功：

```bash
python -c "import mavsdk; print('mavsdk installed')"
```

如果输出：

```text
mavsdk installed
```

说明安装成功。

---

## 4. PX4 SITL MAVLink 端口

Day 39 中，PX4 的 `mavlink status` 显示：

```text
instance #1:
mode: Onboard
transport protocol: UDP (14580, remote port: 14540)
```

因此，本次 MAVSDK Python 程序优先连接：

```text
udp://:14540
```

含义：

```text
MAVSDK 在本机监听 14540
PX4 通过 MAVLink 向 14540 发送数据
```

---

## 5. 连接测试程序

文件路径：

```text
code/03_mavsdk_telemetry/connect_test.py
```

代码：

```python
import asyncio
from mavsdk import System


async def main():
    drone = System()

    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    print("Connection test finished.")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 6. 运行方法

先启动 PX4 SITL：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

再打开另一个终端，进入 MAVSDK 项目目录：

```bash
cd ~/uav-learning/code/03_mavsdk_telemetry
source venv/bin/activate
python connect_test.py
```

成功输出示例：

```text
Connecting to PX4 SITL on udp://:14540 ...
Waiting for drone connection...
Drone connected!
Connection test finished.
```

---

## 7. 如果连接失败

可以尝试把连接地址从：

```python
await drone.connect(system_address="udp://:14540")
```

改成：

```python
await drone.connect(system_address="udpin://0.0.0.0:14540")
```

然后重新运行：

```bash
python connect_test.py
```

---

## 8. 今日理解

今天理解了：

```text
MAVSDK Python 是一个 Python 开发库
它通过 MAVLink 和 PX4 通信
PX4 SITL 的 Onboard MAVLink 实例远端端口是 14540
MAVSDK 程序可以监听 14540 来接收 PX4 数据
```

---

## 9. 今日总结

今天完成了 MAVSDK Python 的安装和最小连接测试。

最重要的结论：

```text
如果程序输出 Drone connected!，说明 MAVSDK Python 已经成功通过 MAVLink 连接到 PX4 SITL。
```

下一步要做：

```text
读取 PX4 telemetry，包括高度、位置、姿态和飞行模式。
```
