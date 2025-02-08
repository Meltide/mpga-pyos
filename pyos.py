import random #随机库
from colorama import Fore, Back #彩色文字库
from pyosLogin import login
from cmdList.registerCmd import registerCmd

class PyOS(login):
    def run(self,cmd):
        match cmd:
            case "cd" | "cd ~":
                self.error = 0
                self.file = "~"
            case "cd ..":
                self.error = 0
                self.file = "/"
            case "cd /":
                self.error = 0
                self.file = "/"
            case "cd home":
                self.error = 0
                self.file = "~"

            case "":
                space = 0

            case _:
                cmdList = registerCmd().shallowCmd
                if cmdList.get(cmd, False) != False:
                    cmdList.get(cmd)(self)
                else:
                    print("Unknown command.")
                    self.error = 1
                    errcode = str(random.randint(100, 999))



if __name__ == "__main__":
    try:
        PyOS()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}You exited PyOS just now!")
