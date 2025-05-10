import os
from colorama import Fore

from utils.config import *
from utils.foxShell import FoxShell

__doc__ = "FoxShell config"

__usage__ = {
    "theme": "Set theme for FoxShell",
    "reload": "Reload FoxShell with fox_config.json"
}

def execute(self, args):
    global theme_list

    if not args:  # 检查是否提供了参数
        FoxShell.show_greeting()
        return
    
    theme_list = [
        "modern",
        "classic",
        "bash"
    ]
    
    match args[0]:
        case "theme":
            if args[1] == "list":
                show_available_themes()
                return
            if args[1] not in theme_list:
                raise SyntaxError(f"Unknown theme: {args[1]}")
                show_avaliable_themes()
                return
            fox["theme"] = args[1]
            with open(os.path.join("configs", "fox_config.json"), "w", encoding="utf-8") as f:
                json.dump(fox, f, ensure_ascii=False, indent=4)
                print(f"• {Fore.GREEN}Theme set successfully.")
                print(f"Type '{Fore.BLUE}fox reload{Fore.RESET}' to apply changes.")
        case "reload":
            FoxShell.reload(self)
        case _:
            raise SyntaxError(f"Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")

def show_available_themes():
    print("Avaliable themes:")
    for theme in theme_list:
        if fox["theme"] == theme:
            print(f"- {Fore.BLUE}{theme} {Fore.RESET}(Current theme)")
            continue
        print(f"- {Fore.BLUE}{theme}")