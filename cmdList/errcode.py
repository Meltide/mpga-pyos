from ..src.pyos.utils.man import ErrorCodeManager
from rich import print

__doc__ = "Return the name of error code"

__usage__ = {
    "[error code]": "Return the name of error code"
}

def execute(self, args):
    if not args:
        raise SyntaxError("No errcode inputed. Please input an errcode.")

    if len(args) >= 1:
        for code in args:
            print("[green]" + str(code), end=": [/]")
            print("[blue]" + str(ErrorCodeManager().get_type(int(code)))+'[/]')
