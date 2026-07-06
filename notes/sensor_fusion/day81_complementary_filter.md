# Day 81 互补滤波小实验

## 今日目标

模拟陀螺仪角速度和加速度计角度，用互补滤波融合得到更稳定的姿态角估计。

---

## 1. 实验背景

Day 80 中已经学习：

- 加速度计可以根据重力方向估计 roll / pitch
- 加速度计长期不漂移，但容易受振动和运动加速度影响
- 陀螺仪可以通过积分得到角度变化
- 陀螺仪短期平滑，但长期会因为 bias 漂移

因此需要将两者融合。

---

## 2. 互补滤波公式

```text
angle = alpha * (angle + gyro_rate * dt) + (1 - alpha) * accel_angle
其中：

angle + gyro_rate * dt：陀螺仪积分预测角度
accel_angle：加速度计估计角度
alpha：滤波权重

当 alpha = 0.98 时，可以理解为：

98% 相信陀螺仪短期变化
2% 用加速度计修正长期漂移
3. 今日代码

代码文件：

code/06_sensor_fusion_basic/complementary_filter_demo.py

运行命令：

cd ~/uav-learning/code/06_sensor_fusion_basic
python3 complementary_filter_demo.py
4. 今日输出

CSV：

data/month3/complementary_filter_data.csv

图像：

plots/month3/complementary_filter.png
5. 实验观察
加速度计角度

现象：

噪声明显
在扰动区间波动更大
长期不会无限漂移

结论：

加速度计适合提供长期参考，但短期不够平滑。

陀螺仪积分角度

现象：

短期比较平滑
随时间产生漂移

结论：

陀螺仪适合估计短期姿态变化，但长期会因为 bias 漂移。

互补滤波角度

现象：

比加速度计更平滑
比陀螺仪积分更不容易漂移
整体更接近真实角度

结论：

互补滤波利用了加速度计和陀螺仪的互补特点。

6. alpha 的影响

alpha 越大：

越相信陀螺仪
曲线更平滑
但漂移修正更慢

alpha 越小：

越相信加速度计
漂移修正更快
但更容易受噪声影响

本实验默认：

alpha = 0.98
7. 今日结论

互补滤波的本质是：

用陀螺仪负责短期姿态变化，用加速度计修正长期漂移。

它是最简单的 IMU 姿态融合方法，也是后续理解 Kalman Filter 和 PX4 EKF2 的基础。


---

# 10. 今日完成标准

今天完成后，你应该有：

```text
code/06_sensor_fusion_basic/complementary_filter_demo.py
data/month3/complementary_filter_data.csv
plots/month3/complementary_filter.png
notes/sensor_fusion/day81_complementary_filter.md

你应该能回答：

1. 为什么只用加速度计会抖？
2. 为什么只用陀螺仪会漂？
3. 互补滤波公式每一项是什么意思？
4. alpha 越大代表什么？
5. 为什么互补滤波适合做 IMU 姿态入门实验？
