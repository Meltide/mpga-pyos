<div align="center">

<img src="res/logo.png" height="114px">

# MPGA PyOS
![GitHub repo size](https://img.shields.io/github/repo-size/Meltide/mpga-pyos)
![GitHub Repo stars](https://img.shields.io/github/stars/Meltide/mpga-pyos?style=flat)
![GitHub branch status](https://img.shields.io/github/checks-status/Meltide/mpga-pyos/main)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/Meltide/mpga-pyos)
![GitHub last commit](https://img.shields.io/github/last-commit/Meltide/mpga-pyos)
![GitHub Created At](https://img.shields.io/github/created-at/Meltide/mpga-pyos) 
### 颠覆想象，焕然新生

**M**ake **P**yOS **G**reat **A**gain
<br>
让 PyOS 再次伟大！

</div>

## 使用方法

### 方法1

0. 确保已经安装了 Python 3
1. （可选，使用步骤3更佳）输入命令`pip install -r requirements.txt`来安装依赖
2. 转到 PyOS 所在的目录
3. （可选）输入`.\install.sh`来安装[子模块](https://github.com/Meltide/mpga-apps)和依赖
4. （可选）输入`.\update.sh`来更新[子模块](https://github.com/Meltide/mpga-apps)
5. 输入 `python pyos.py` 来启动

### 方法2

> [!TIP]
> 此方案需要 Nix

0. 转到 PyOS 所在的目录
1. 输入 `nix-shell` 进入 Nix Shell 环境
2. 输入 `python3 pyos.py` 来启动

> [!WARNING]
> 必须在 `pyos.py` 所在的目录下运行该文件，且不要尝试运行除 `pyos.py` 以外的其他文件，否则可能会因为绝对引用而报错

用户名：**root**
<br>
初始密码：**114514**

输入 `help` 获取帮助

## 界面截图
![ui1](res/ui1.jpg)
![ui2](res/ui2.jpg)

----
注意：  
- 2.0版本开始 **不再提供** 已编译exe文件，请直接下载源码！   
- 请确保 **您的 Python 版本 >= 3.10** ！
