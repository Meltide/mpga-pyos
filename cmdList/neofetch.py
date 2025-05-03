from colorama import Fore, Back #彩色文字库
import time #时间库
import psutil
from cmdList.sysname import execute as sysname
from art import text2art

__doc__="List all hardware and system version"

def execute(self,args):
    print(Fore.BLUE+text2art("MPGA"))
    print(f"{Fore.BLUE}root{Fore.RESET}@{Fore.BLUE}{self.hostname}")
    print("-----------------")
    time.sleep(0.05)
    print(f"{Fore.BLUE}OS{Fore.RESET}: MPGA PyOS V{self.version} aarch64")
    match sysname(self,args):
        case 1:
            host = "Windows CMD"
        case 2:
            host = "POSIX Shell"
        case _:
            host = "Unknown"
    time.sleep(0.05)
    print(f"{Fore.BLUE}Host{Fore.RESET}: {host}")
    print(f"{Fore.BLUE}Kernel{Fore.RESET}: PTCORE-V{self.core_version}-aarch64")
    time.sleep(0.05)
    print(f"{Fore.BLUE}Shell{Fore.RESET}: pysh {self.shell_version}")
    time.sleep(0.05)
    print(f"{Fore.BLUE}CPU{Fore.RESET}: ({psutil.cpu_count()}) @ {psutil.cpu_freq().max  / (1024):.2f}Ghz")
    time.sleep(0.05)
    print(f"{Fore.BLUE}Memory{Fore.RESET}: {psutil.virtual_memory().used / (1048576):.2f}MiB/{psutil.virtual_memory().total / (1048576):.2f}MiB")
    time.sleep(0.05)
    print("")
    print(
        Back.BLACK
        + "    "
        + Back.RED
        + "    "
        + Back.GREEN
        + "    "
        + Back.YELLOW
        + "    "
        + Back.BLUE
        + "    "
        + Back.MAGENTA
        + "    "
        + Back.CYAN
        + "    "
        + Back.WHITE
        + "    "
    )
    print("")
