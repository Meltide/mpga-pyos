from cmdList.registerCmd import registerCmd
from colorama import Fore, Back #彩色文字库
import time #时间库
import psutil

def neofetch(self):
    self.error = 0
    print(f"{Fore.BLUE}  __  __ ____   ____    _    \n |  \\/  |  _ \\ / ___|  / \\   \n | |\\/| | |_) | |  _  / _ \\  \n | |  | |  __/| |_| |/ ___ \\ \n |_|  |_|_|    \\____/_/   \\_\\\n                             ")
    print(f"{Fore.BLUE}root{Fore.RESET}@{Fore.BLUE}{self.hostname}")
    print("-----------------")
    time.sleep(0.05)
    print(f"{Fore.BLUE}OS{Fore.RESET}: MPGA PyOS V{self.ver} aarch64")
    if self.cls == 1:
        host = "Windows CMD"
    elif self.cls == 2:
        host = "POSIX Shell"
    else:
        host = "Unknown"
    time.sleep(0.05)
    print(f"{Fore.BLUE}Host{Fore.RESET}: {host}")
    print(f"{Fore.BLUE}Kernel{Fore.RESET}: PTCORE-V{self.core}-aarch64")
    time.sleep(0.05)
    print(f"{Fore.BLUE}Shell{Fore.RESET}: pysh {self.pyshver}")
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

registerCmd().register("neofetch", "List all hardware and system version", "System", neofetch)