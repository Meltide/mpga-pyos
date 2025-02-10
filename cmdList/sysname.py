import os

def execute(self,args):
    if os.name == "nt": #Windows系统
        return 1
    else: #其他系统
        return 2