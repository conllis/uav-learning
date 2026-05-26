# Day 25 学习坐标系 NED / ENU / 机体系

## 今日目标

理解无人机中常见坐标系，包括 NED、ENU、FRD、FLU，以及世界系和机体系之间的区别。

---

## 1. 什么是坐标系？

坐标系是对“前后、左右、上下”的约定。

同一个物体位置，在不同坐标系下数字可能不同，但物理位置不变。

---

## 2. NED 坐标系

NED = North East Down

```text
X：North，北
Y：East，东
Z：Down，下

特点：

Z 轴向下为正
无人机上升时，z 可能变小

PX4 中常见 NED 表示。

3. ENU 坐标系

ENU = East North Up

X：East，东
Y：North，北
Z：Up，上

特点：

Z 轴向上为正
无人机上升时，z 变大

ROS 中常见 ENU 表示。

4. NED 和 ENU 转换
x_enu = y_ned
y_enu = x_ned
z_enu = -z_ned

反过来：

x_ned = y_enu
y_ned = x_enu
z_ned = -z_enu
5. 机体系 FRD

FRD = Forward Right Down

X：Forward，机头前方
Y：Right，机体右方
Z：Down，机体下方

PX4 常用 FRD 机体系。

6. 机体系 FLU

FLU = Forward Left Up

X：Forward，机头前方
Y：Left，机体左方
Z：Up，机体上方

ROS 常用 FLU 机体系。

7. FRD 和 FLU 转换
x_flu = x_frd
y_flu = -y_frd
z_flu = -z_frd
8. 世界系和机体系区别
世界系：固定不动
机体系：跟着无人机旋转

如果无人机 yaw 改变，机体系的前方也会随之改变。

9. Day 25 C++ 实验

项目路径：

code/cpp/day25_coordinate_frames

编译运行：

cd ~/uav-learning/code/cpp/day25_coordinate_frames
cmake -S . -B build
cmake --build build
./build/day25_coordinate_frames

实验内容：

NED 转 ENU
ENU 转 NED
FRD 转 FLU
FLU 转 FRD
机体系速度根据 yaw 转成 NED 世界系速度
10. 今日总结

今天理解了无人机中几个关键坐标系。

最重要的结论：

NED：北、东、下
ENU：东、北、上
FRD：前、右、下
FLU：前、左、上
世界系固定不动
机体系跟着无人机转

在 PX4 / ROS / Gazebo / Offboard 控制中，如果坐标系搞错，无人机就可能朝错误方向飞。


---

# 十三、提交 Day 25
