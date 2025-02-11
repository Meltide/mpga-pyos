import random #随机库
from colorama import Fore, Back #彩色文字库
from pyosLogin import login
from cmdList.help import execute as doc

def execute(cmd,args=()):
    '''支持带参数的命令'''
    __import__('cmdList.'+cmd,fromlist=["execute"]).execute(*args)

class PyOS(login):
    def run(self,cmds:str):
        try:
            cmd=cmds.split(' ')
            cmdname = cmd[0]
            if cmdname:
                self.error = 0
                if len(cmd) > 1:
                    if cmd[1]=='-h':
                        execute('help',(self,[cmdname]))
                    else:
                        execute(cmdname,(self,cmd[1:]))
                else:
                    execute(cmdname,(self,[]))
            else:
                space = 0
        except ImportError:
            print("Unknown command.")
            self.error = 1
            errcode = str(random.randint(100, 999))
            
                



if __name__ == "__main__":
    try:
        PyOS()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}You exited PyOS just now!")
