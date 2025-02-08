from cmdList.registerCmd import registerCmd
import sys #系统底层库
import time #时间库
from colorama import Fore #彩色文字库

def shutdown(self):
    self.error = 0
    print(Fore.BLUE + "Shutting down")
    for i in range(5):
        print(".", end="")
        time.sleep(0.5)
    self.clear()
    sys.exit(0)

registerCmd().register("shutdown", "Shutdown the system", "Power", shutdown)