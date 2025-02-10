import os

def execute(args):
    if os.name == "nt": #Windows系统
        return 1
    else: #其他系统
        return 2