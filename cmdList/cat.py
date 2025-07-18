from colorama import Fore
from utils.man import ErrorCodeManager

__doc__ = "Catch file's content"

__usage__ = {
    "[filename]": "Catch file's content"
}

def execute(self, args):
    if not args:
        print(
            f"Error: {Fore.RED}No filename provided. Please specify a valid command."
        )
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    with open(args[0], "r") as f:
        for line in f:
            print(line, end="")
        print()