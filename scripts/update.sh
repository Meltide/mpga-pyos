#!/bin/bash

echo "Updating submodules..."
git submodule init
git submodule update --remote --recursive
git submodule foreach git pull origin main
read -p "Done."