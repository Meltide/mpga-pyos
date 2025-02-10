from pyos import PyOS
from cmdList.clear import execute as clear
__doc__="Restart PyOS"
def execute(self):
    clear(self)
    PyOS()
