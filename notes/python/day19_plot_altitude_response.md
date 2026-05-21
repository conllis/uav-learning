# Day 19 画高度响应曲线

## 今日目标

读取 Day 18 高度控制仿真生成的 CSV 文件，并画出高度响应曲线、误差曲线、速度曲线和推力曲线。

---

## 1. 输入数据

Day 18 输出文件：

```bash
code/cpp/day18_altitude_control_sim/altitude_control_result.csv

CSV 字段：

time,setpoint,altitude,velocity,acceleration,thrust,error
2. 画图脚本

脚本路径：

code/python/day19_plot_altitude_response/plot_altitude_response.py

运行：

cd ~/uav-learning/code/python/day19_plot_altitude_response
python3 plot_altitude_response.py
3. 输出图片
figures/day19/altitude_response.png
figures/day19/altitude_error.png
figures/day19/velocity_response.png
figures/day19/thrust_response.png
4. 高度响应曲线怎么看？

高度响应曲线中：

Target altitude 是目标高度
Actual altitude 是实际高度

需要观察：

上升时间
超调
稳态误差
调节时间
是否震荡
5. 几个重要概念
上升时间

高度从初始值接近目标高度所需的时间。

超调

实际高度超过目标高度的最大值。

稳态误差

最终高度和目标高度之间的差值。

调节时间

系统进入目标附近并基本稳定所需的时间。

6. 今日理解

PID 参数会影响高度响应：

kp 大，响应更快，但可能超调
ki 可以减小稳态误差，但太大会导致超调
kd 可以抑制震荡，但太大会让系统变慢或对噪声敏感
今日总结

今天完成了高度控制仿真结果的可视化。相比只看 CSV，曲线能更直观地展示控制器响应速度、超调、稳态误差和推力变化。

这一步是从“写控制器”走向“分析控制器性能”的关键。


---
