import json
import os
from colorama import Fore  # 彩色文字库

from utils.man import ErrorCodeManager
from utils.config import profiles  # 直接导入 profiles

__doc__ = "PyOS Host Manager"

__usage__ = {
    "hostname": "Show current hostname",
    "change": "Change your hostname",
}


def execute(self, args):
    if not args:  # 检查是否提供了参数
        print(
            f"Error: {Fore.RED}No arguments provided. Please specify a valid command."
        )
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    match args[0]:
        case "hostname":
            print(f"Current hostname: {Fore.GREEN}{profiles['hostname']}")
        case "change":
            self.hostname = input("Type new hostname: ")
            profiles["hostname"] = self.hostname
            with open(
                os.path.join("configs", "profiles.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(profiles, f, ensure_ascii=False, indent=4)

            print(f"{Fore.GREEN}Hostname changed successfully.")
        case _:
            print(f"Error: {Fore.RED}Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)
