import os
from . import sysname

__doc__="Clean the screen"

def execute(self,args):
    os.system('cls' if sysname.execute(self,args)==1 else 'clear')
