import sys #系统底层库

from . import clear
__doc__="Log out"
def execute(args):
    clear.execute(args)
    sys.exit(0)
