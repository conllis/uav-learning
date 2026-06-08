# Day 39 启动 PX4 SITL 并确认 MAVLink 端口

## 今日目标

今天的目标是启动 PX4 SITL，确认 PX4 是否正常运行，并查看 MAVLink 通信端口，为后续使用 MAVSDK 连接 PX4 做准备。

---

## 1. 启动 PX4 SITL

启动命令：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

启动成功后，应看到：

```text
Gazebo Sim 可视化界面
PX4 终端输出
pxh>
```

其中，`pxh>` 是 PX4 的命令行提示符，可以在里面输入 PX4 内部命令。

---

## 2. 检查 PX4 是否运行

在 `pxh>` 中输入：

```bash
commander status
```

或者：

```bash
uorb top
```

如果能看到飞控状态或 uORB topic 信息，说明 PX4 正常运行。

---

## 3. 查看 MAVLink 状态

在 `pxh>` 中输入：

```bash
mavlink status
```

重点观察输出中的：

```text
UDP
14540
14550
14580
```

不同 PX4 版本输出可能不同，但通常可以看到多个 MAVLink 实例。

---

## 4. MAVLink 端口理解

常见端口含义：

```text
14550：通常用于 QGroundControl 地面站连接
14540：通常用于 MAVSDK / Offboard API 连接
14580 / 18570：可能是 PX4 内部或其他 MAVLink 实例端口
```

后续 MAVSDK Python 程序通常会尝试连接：

```text
udp://:14540
```

但最终以 `mavlink status` 的实际输出为准。

---

## 5. 使用 Linux 命令查看 UDP 端口

在另一个终端中执行：

```bash
ss -lunp | grep -E '14540|14550|14580|18570'
```

这个命令用于查看当前系统中的 UDP 监听端口。

如果没有输出，可以尝试：

```bash
ss -lunp | grep udp
```

---

## 6. QGroundControl 连接检查

打开 QGroundControl 后，观察是否自动连接 PX4 SITL。

可以检查：

```text
是否显示无人机图标
是否显示飞行模式
是否显示高度 / 姿态
是否能查看参数
```

如果 QGroundControl 能连接，说明 PX4 SITL 的 MAVLink 地面站通信正常。

---

## 7. 今日记录

本次启动命令：

```text
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

Gazebo 是否打开：

```text
是 / 否：
```

是否出现 `pxh>`：

```text
是 / 否：
```

`mavlink status` 中看到的端口：

```text
14540：
14550：
14580：
其他：
```

QGroundControl 是否连接：

```text
是 / 否：
```

后续 MAVSDK 准备使用的连接地址：

```text
udp://:14540
```

---

## 8. 今日总结

今天理解了 PX4 SITL 启动后会通过 MAVLink 对外通信。

最重要的结论：

```text
QGroundControl 和 MAVSDK 都是通过 MAVLink 与 PX4 通信；
QGroundControl 通常使用 14550；
MAVSDK 常用 udp://:14540；
实际端口需要通过 mavlink status 确认。
```

一句话总结：

```text
Day 39 的核心是确认 PX4 SITL 的 MAVLink 通信入口，为后续 MAVSDK 连接 PX4 做准备。
```
