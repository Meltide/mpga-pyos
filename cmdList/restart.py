from src.pyos.core.pyos import PyOS
from cmdList.clear import execute as clear

__doc__ = "Restart PyOS"


def execute(self, args):
    clear(self, args)
    PyOS()
