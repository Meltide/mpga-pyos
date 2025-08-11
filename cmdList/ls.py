import os  # 系统底层库
from rich import print  # 颜色库

__doc__ = "View the path"

__usage__ = {
    "[path]": "View the contents from path",
}

def execute(self, args):
    if not args:
        items = os.listdir(os.getcwd())
    else:
        items = os.listdir(args[0])

    # 分离文件夹和文件，并按名称排序（不区分大小写）
    folders = sorted(
        [item for item in items if os.path.isdir(item)],
        key=lambda x: x.lower(),  # 按文件名排序（忽略大小写）
    )
    files = sorted(
        [item for item in items if not os.path.isdir(item)],
        key=lambda x: x.lower(),  # 按文件名排序（忽略大小写）
    )

    for folder in folders:
        print("[blue]" + folder + "/[/]", end="\n")

    for file in files:
        print(file)
