#!/bin/bash
#第一次下载源代码时，执行该脚本

echo "Downloading submodules..."
git submodule init
git submodule update --recursive

echo "Downloading dependencies..."
pip install -r requirements.txt
read -p "Press enter to exit..."