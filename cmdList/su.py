import pwinput
import base64
from rich import print

from utils.config import *
from utils.man import ErrorCodeManager
from utils.foxShell import FoxShell

__doc__ = "Switch user"

__usage__ = {
    "[username]": "Switch to target user"
}

def execute(self, args):
    if not args:  # 检查是否提供了参数
        print("Error: [red]No arguments provided. Please specify a valid command.[/]")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return
    
    if args[0] not in ACCOUNT_NAMES:
        raise NameError(f"Invaild username: '{args[0]}'")
    
    stpasswd = base64.b64decode(profiles["accounts"][args[0]]["passwd"].strip()).decode(
        "utf-8"
    )
    passwd = pwinput.pwinput("Password: ")
    if passwd != stpasswd:
        raise ValueError("Password incorrect.")
    
    self.username = args[0]
    self.group = ACCOUNTS[args[0]]["group"]
    self.load_user_profiles(args[0])
    
    FoxShell.reload(self, True)
    FoxShell.show_greeting(self)