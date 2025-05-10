import json
from colorama import Fore, Style
from utils.config import *
from utils.man import ErrorCodeManager

__doc__ = "Set system policy"

__usage__ = {
    "enable": "Enable policys",
    "disable": "Disable policys",
    "list": "Show all policys"
}

def execute(self, args):
    if not args:  # 检查是否提供了参数
        print(f"Error: {Fore.RED}No arguments provided. Please specify a valid command.")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return
    
    match args[0]:
        case "enable":
            set_status(self, True, args[1:])
        case "disable":
            set_status(self, False, args[1:])
        case "list":
            print("All system policys:")
            for policy, status in policys.items():
                print(f"- {Fore.BLUE}{policy}{Fore.RESET}: {Fore.YELLOW}{status}")
            print(f"Error: {Fore.RED}Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)

def set_status(self, status, args):
    if not args:
        raise SyntaxError("No settings inputed.")
        return

    try:
        with open(os.path.join("configs", "system_policys.json"), "w", encoding='utf-8') as f:
            policys[args[0]] = status
            json.dump(policys, f, ensure_ascii=False, indent=4)
            print(f"The new status of {Fore.BLUE}{args[0]}{Fore.RESET}: {Fore.YELLOW}{status}")
            print(Style.DIM + "It will take effect after restarting the system.")
    except Exception as e:
        print(f"Error: {Fore.RED}{e}")
        self.error_code = ErrorCodeManager.get_code(e)