from rich import print  # 彩色文字库
import time  # 时间库
import psutil
from cmdList.sysname import execute as sysname
from utils.config import *
from art import text2art

__doc__ = "List all hardware and system version"


def execute(self, args):
    print('[blue]' + text2art("MPGA")+'[/]')
    print(f"[blue]root[/]@[blue]{self.hostname}[/]")
    print("-----------------")
    time.sleep(0.05)
    print(f"[blue]OS[/]: MPGA PyOS V{self.version} aarch64")
    match sysname(self, args):
        case 1:
            host = "Windows CMD"
        case 2:
            host = "POSIX Shell"
        case _:
            host = "Unknown"
    time.sleep(0.05)
    print(f"[blue]Host[/]: {host}")
    print(f"[blue]Kernel[/]: PTCORE-V{self.core_version}-aarch64")
    time.sleep(0.05)
    print(f"[blue]Package[/]: {get_package_count()}")
    time.sleep(0.05)
    print(f"[blue]Shell[/]: FoxShell {self.shell_version}")
    time.sleep(0.05)
    print(
        f"[blue]CPU[/]: ({psutil.cpu_count()}) @ {psutil.cpu_freq().max  / (1024):.2f}Ghz"
    )
    time.sleep(0.05)
    print(
        f"[blue]Memory[/]: {psutil.virtual_memory().used / (1048576):.2f}MiB/{psutil.virtual_memory().total / (1048576):.2f}MiB"
    )
    time.sleep(0.05)
    print("")
    print("[on black]    [/][on red]    [/][on green]    [/][on yellow]    [/][on blue]    [/][on magenta]    [/][on cyan]    [/][on white]    [/]")
    print("")


def get_package_count():
    third_party_dir = os.path.join("cmdList", "third_party")
    if not os.path.exists(third_party_dir):
        return 0
    return len(os.listdir(third_party_dir))
