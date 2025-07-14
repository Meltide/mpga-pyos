import sys
from colorama import Fore, Style
from utils.man import ErrorCodeManager

__doc__ = "Execute python commands"

__usage__ = {
    "[command]": "Python commands to be run",
}

def execute(self, args):
    if not args:
        start_exec_shell(self)
        return
    exec_cmd(self, args[0])

def start_exec_shell(self):
    print(Fore.BLUE + "MPGA Python Command Executor")
    print(f"Python version: {sys.version}")
    print(Style.DIM + "Type 'exit' to exit\n")

    while True:
        if (py_cmd := input(">>> ")) == "exit":
            return
        exec_cmd(self, py_cmd)
        
def exec_cmd(self, cmd):
    try:
        result = eval(str(cmd))
        if result is not None:
            print(result)
            return
        result = exec(str(cmd))
    except Exception as e:
        print(f"Error: {Fore.RED}{e if str(e) else type(e).__name__}")
        self.error_code = ErrorCodeManager().get_code(e)