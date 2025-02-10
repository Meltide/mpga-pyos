import random #随机库
from colorama import Fore, Back #彩色文字库
from pyosLogin import login
from cmdList.help import execute as doc

def execute(cmd,args=()):
    '''支持带参数的命令'''
    __import__('cmdList.'+cmd,fromlist=["execute"]).execute(*args)

class PyOS(login):
    def run(self,cmds:str):
        cmd=cmds.split(' ')
        #print(cmd)
        match cmd[0]:
            case "":
                space = 0
            case "help":
                if len(cmd) > 1:
                    doc(self,cmd[1:])
                else:
                    doc(self,[])
            case _:
                try:
                    self.error = 0
                    if len(cmd) > 1:
                        execute(cmd[0],(self,cmd[1:]))
                    else:
                        execute(cmd[0],(self,[]))
                except ImportError:
                    print("Unknown command.")
                    self.error = 1
                    errcode = str(random.randint(100, 999))



if __name__ == "__main__":
    try:
        PyOS()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}You exited PyOS just now!")
