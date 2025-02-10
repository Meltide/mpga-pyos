import os
from . import sysname

__doc__="Clean the screen"

def execute(args):
    os.system('cls' if sysname.execute(args)==1 else 'clear')
