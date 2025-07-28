__doc__ = "Run PYOScript files(.pyos)"

__usage__ = {
    "": "Start PYOScript shell",
    "[code]": "Run PYOScript code",
    "-r [path]": "Run PYOScript files from the path"
}

import os
from ..src.pyos.utils.safety import rich_input
from ..src.pyos.utils.config import *
from ..src.pyos.utils.man import ErrorCodeManager
from PYOScript.interpreter import PYOScriptInterpreter as PSI


def execute(self, args):
    if not args:
        quit_ = False
        while not quit_:
            code = rich_input(f"[green]PYOScript[/]> ")
            if code.strip() == "exit":
                quit_ = True
            else:
                script = PSI(code)
                script.parse()
                script.run()
        return
    
    script = PSI(args[0])
    if os.path.isfile(args[0]):
        script.parse()
    script.run()
