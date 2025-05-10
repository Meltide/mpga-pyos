import os  # 系统底层库
from colorama import Fore, Style  # 颜色库

__doc__ = "View the path"

def execute(self, args):
    items = os.listdir(os.getcwd())
    
    # 分离文件夹和文件，并按名称排序（不区分大小写）
    folders = sorted(
        [item for item in items if os.path.isdir(item)],
        key = lambda x: x.lower()  # 按文件名排序（忽略大小写）
    )
    files = sorted(
        [item for item in items if not os.path.isdir(item)],
        key = lambda x: x.lower()  # 按文件名排序（忽略大小写）
    )
    
    for folder in folders:
        print(Fore.BLUE + folder, end="/\n")

    for file in files:
        print(file)