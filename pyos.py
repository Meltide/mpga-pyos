import random #随机库
from colorama import Fore #彩色文字库
from pyosLogin import login
import traceback

class PyOS(login):
    def run(self,cmds:str):
        try:
            cmd=cmds.split(' ')
            cmdname = cmd[0]
            self.cmdman.reg(cmdname)
            if cmdname:
                self.error = 0
                if len(cmd) > 1:
                    if cmd[1]=='-h':
                        self.cmdman.reg("help")
                        self.cmdman.execute((self,[cmdname]))
                    else:
                        self.cmdman.execute((self,cmd[1:]))
                else:
                    self.cmdman.execute((self,[]))
            else:
                space = 0
        except ImportError:
            self.fprint("Unknown command.",3)
        except BaseException:
            self.fprint(traceback.format_exc(),3)

if __name__ == "__main__":
    try:
        PyOS()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}You exited PyOS just now!")
