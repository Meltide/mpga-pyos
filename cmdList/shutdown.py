import sys #系统底层库
from cmdList.clear import execute as clear

__doc__="Shutdown the system"

def execute(self,args):
    sys.exit(0)
