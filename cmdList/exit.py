import sys  # 系统底层库
from . import clear

__doc__ = "Log out"


def execute(self, args):
    clear.execute(self, args)
    sys.exit(0)
