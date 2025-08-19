#!/bin/bash
#第一次下载源代码时，若没有子模块和所有依赖模块，执行该脚本

echo "Downloading submodules..."
git submodule init
git submodule update --recursive

echo "Downloading dependencies..."
pip install -r requirements.txt

# 仅在交互式终端中暂停
if [ -t 0 ]; then
    read -p "Press enter to exit..."
fi