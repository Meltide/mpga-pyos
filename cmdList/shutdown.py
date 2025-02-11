import sys #系统底层库
import time #时间库
from colorama import Fore #彩色文字库
from cmdList.clear import execute as clear

__doc__="Shutdown the system"

def execute(self,args):
    print(Fore.BLUE + "Shutting down")
    for i in range(5):
        print(".", end="")
        time.sleep(0.5)
    clear(self,args)
    sys.exit(0)
