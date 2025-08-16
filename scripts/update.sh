#!/bin/bash

echo "Updating submodules..."
git submodule init
git submodule update --remote --recursive
git submodule foreach git pull origin main

# 仅在交互式终端中暂停
if [ -t 0 ]; then
    read -p "Press enter to exit..."
fi