import os
from colorama import Fore

from utils.man import ErrorCodeManager
from utils.config import *
from utils.foxShell import FoxShell

__doc__ = "FoxShell config"

__usage__ = {"theme": "Set theme for FoxShell", "reload": "Reload FoxShell"}


def execute(self, args):
    global theme_list

    if not args:  # 检查是否提供了参数
        FoxShell.show_greeting()
        return

    theme_list = ["modern", "classic", "bash"]

    match args[0]:
        case "theme":
            if args[1] == "list":
                show_available_themes()
                return
            if len(args) < 2:
                raise SyntaxError("Please input a theme.")
                return
            elif args[1] not in theme_list:
                print(f"Unknown theme: {args[1]}")
                show_available_themes()
                self.error_code = ErrorCodeManager().get_code(SyntaxError)
                return
            fox["theme"] = args[1]
            with open(
                os.path.join("configs", "fox_config.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(fox, f, ensure_ascii=False, indent=4)
                print(f"• {Fore.GREEN}Theme set successfully.")
        case "reload":
            FoxShell.reload(self)
        case _:
            print(f"Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)


def show_available_themes():
    print("Avaliable themes:")
    for theme in theme_list:
        if fox["theme"] == theme:
            print(f"- {Fore.BLUE}{theme} {Fore.RESET}(Current theme)")
            continue
        print(f"- {Fore.BLUE}{theme}")
