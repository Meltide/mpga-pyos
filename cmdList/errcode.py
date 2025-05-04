from utils.man import ErrorCodeManager 
from colorama import Fore
__doc__="Return the name of error code"

def execute(self, args):
    if not args:
        print(f"Error: {Fore.RED}No errcode inputed. Please input an errcode.")
        return

    if len(args) >= 1:
        for code in args:
            print(Fore.GREEN+str(code),end=": ")
            print(Fore.BLUE+str(ErrorCodeManager().get_type(int(code))))