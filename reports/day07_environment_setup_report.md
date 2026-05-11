# Day 07 无人机飞控学习环境搭建报告

## 一、当前环境

| 项目 | 内容 |
|---|---|
| 主机系统 | Windows |
| Linux 环境 | WSL Ubuntu |
| 用户名 | zzz |
| 学习仓库 | `~/uav-learning` |
| PX4 源码目录 | `~/PX4-Autopilot` |
| Gazebo 版本 | Gazebo Sim 8.11.0 |
| PX4 仿真目标 | `px4_sitl gz_x500` |

---

## 二、学习环境总体结构

```text
Windows
├── VS Code
├── QGroundControl，后续安装
└── WSL Ubuntu
    ├── ~/uav-learning
    │   ├── notes/
    │   ├── reports/
    │   ├── code/
    │   └── scripts/
    └── ~/PX4-Autopilot
        ├── src/
        ├── Tools/
        ├── ROMFS/
        └── build/
```

---

## 三、WSL Ubuntu 基础环境

### 1. 进入 WSL

```powershell
wsl
```

### 2. 确认系统信息

```bash
whoami
pwd
lsb_release -a
```

### 3. 更新系统

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 四、Git 配置

### 1. 安装 Git

```bash
sudo apt install -y git
```

### 2. 配置用户名和邮箱

```bash
git config --global user.name "zzz"
git config --global user.email "你的邮箱"
```

### 3. 配置默认分支

```bash
git config --global init.defaultBranch main
```

### 4. GitHub SSH 443 配置

由于普通 SSH 22 端口可能连接不稳定，使用 443 端口连接 GitHub。

```bash
mkdir -p ~/.ssh
nano ~/.ssh/config
```

内容：

```text
Host github.com
  HostName ssh.github.com
  User git
  Port 443
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

设置权限：

```bash
chmod 600 ~/.ssh/config
```

测试：

```bash
ssh -T git@github.com
```

---

## 五、VS Code 配置

### 1. Windows 安装 VS Code

在 Windows 中安装 VS Code，并安装 WSL 扩展。

### 2. 从 WSL 打开项目

```bash
cd ~/uav-learning
code .
```

VS Code 左下角应显示：

```text
WSL: Ubuntu
```

---

## 六、C/C++、CMake、Python 环境

### 1. 安装基础工具

```bash
sudo apt install -y build-essential gdb cmake make ninja-build pkg-config
sudo apt install -y python3 python3-pip python3-venv
```

### 2. 检查版本

```bash
gcc --version
g++ --version
gdb --version
cmake --version
ninja --version
python3 --version
pip3 --version
```

### 3. Python pip 镜像源配置

```bash
python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python3 -m pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
python3 -m pip config set global.timeout 120
```

---

## 七、PX4-Autopilot 安装过程

### 1. 克隆 PX4 主仓库

```bash
cd ~
git clone git@github.com:PX4/PX4-Autopilot.git
```

### 2. 配置 GitHub HTTPS 自动改走 SSH

PX4 的很多 submodule 默认使用 HTTPS，容易因为网络问题失败，所以配置：

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### 3. 拉取子模块

```bash
cd ~/PX4-Autopilot
git submodule sync --recursive
git submodule update --init --recursive --jobs 1
```

如果失败，重复执行：

```bash
git submodule update --init --recursive --jobs 1
```

---

## 八、PX4 Python 依赖处理

### 1. 手动安装 PX4 requirements

```bash
cd ~/PX4-Autopilot
python3 -m pip install --user -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r Tools/setup/requirements.txt
```

### 2. 如果某个包失败，单独安装

例如：

```bash
python3 -m pip install --user -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn argcomplete
python3 -m pip install --user -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn cerberus
```

---

## 九、运行 PX4 官方安装脚本

```bash
cd ~/PX4-Autopilot
bash ./Tools/setup/ubuntu.sh
```

脚本结束后重启 WSL：

```powershell
wsl --shutdown
wsl
```

---

## 十、Gazebo 与 OpenCV 依赖

### 1. 检查 Gazebo

```bash
gz sim --version
```

当前结果：

```text
Gazebo Sim, version 8.11.0
```

### 2. 安装 Gazebo 相关开发包

```bash
sudo apt update
sudo apt install -y protobuf-compiler libprotobuf-dev
sudo apt install -y gz-harmonic
sudo apt install -y libgz-transport13-dev libgz-sim8-dev libgz-sensors8-dev libgz-plugin2-dev
```

### 3. 安装 OpenCV

```bash
sudo apt install -y libopencv-dev python3-opencv
```

检查：

```bash
pkg-config --modversion opencv4
```

---

## 十一、编译 PX4 SITL

```bash
cd ~/PX4-Autopilot
make px4_sitl
```

成功后可能显示：

```text
ninja: no work to do.
```

这不是错误，表示已经编译完成，没有新的内容需要重新编译。

---

## 十二、启动 PX4 + Gazebo x500 仿真

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

成功标志：

```text
INFO  [init] Gazebo simulator 8.11.0
INFO  [init] Starting gz gui
INFO  [init] Gazebo world is ready
INFO  [init] Spawning Gazebo model
INFO  [gz_bridge] world: default, model: x500_0
pxh>
```

如果电脑性能不足或图形界面无法打开，可以使用：

```bash
HEADLESS=1 make px4_sitl gz_x500
```

---

## 十三、常见问题记录

### 1. git clone HTTPS 失败

报错：

```text
gnutls_handshake() failed
```

解决：

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

并使用 SSH 克隆：

```bash
git clone git@github.com:PX4/PX4-Autopilot.git
```

---

### 2. submodule 失败

解决：

```bash
cd ~/PX4-Autopilot
git submodule sync --recursive
git submodule update --init --recursive --jobs 1
```

---

### 3. pip 找不到 argcomplete / cerberus

解决：

```bash
python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python3 -m pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
python3 -m pip config set global.timeout 120
```

然后：

```bash
cd ~/PX4-Autopilot
python3 -m pip install --user -r Tools/setup/requirements.txt
```

---

### 4. unknown target gz_x500

原因：

Gazebo 依赖安装前已经生成过 CMake 缓存。

解决：

```bash
cd ~/PX4-Autopilot
make distclean
make px4_sitl
make px4_sitl gz_x500
```

---

### 5. Could NOT find OpenCV

解决：

```bash
sudo apt install -y libopencv-dev python3-opencv
cd ~/PX4-Autopilot
make distclean
make px4_sitl
```

---

### 6. No connection to the GCS

现象：

```text
Preflight Fail: No connection to the GCS
```

原因：

还没有打开 QGroundControl。

下一步：

安装并连接 QGroundControl。

---

## 十四、当前完成状态

| 项目 | 状态 |
|---|---|
| WSL Ubuntu | 已完成 |
| Git 配置 | 已完成 |
| VS Code WSL | 已完成 |
| C/C++ / CMake / Python | 已完成 |
| PX4-Autopilot 主仓库 | 已完成 |
| PX4 submodule | 基本完成 |
| PX4 Python 依赖 | 已完成 |
| Gazebo Sim | 已完成 |
| OpenCV | 已完成 |
| `make px4_sitl` | 成功 |
| `make px4_sitl gz_x500` | 成功 |
| Gazebo 可视化界面 | 成功弹出 |
| QGroundControl | 未开始 |

---

## 十五、下一步计划

Day 8：

```text
安装 QGroundControl
连接 PX4 SITL
查看无人机状态
尝试 Arm / Takeoff / Land
```
