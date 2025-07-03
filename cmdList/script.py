__doc__ = "Run PYOScript files(.pyos)"

__usage__ = {
    "[path]": "Run PYOScript files from the path"
}

import os
from colorama import Fore
from utils.config import *
from utils.man import ErrorCodeManager
from PYOScript.compiler import PSC


def execute(self, args):
    if not args:
        print(f"Error: {Fore.RED}No file selected. Please input a file path.")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    script = PSC(args[0])
    if os.path.isfile(args[0]):
        script.read()
    script.run()
