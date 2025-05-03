from utils.man import ErrorCodeManager 
from colorama import Fore,Back
__doc__="Return the name of error code"

def execute(self, args):
    if len(args) >= 1:
        for code in args:
            print(Fore.GREEN+str(code),end=": ")
            print(Back.BLUE+str(ErrorCodeManager().get_type(int(code))))