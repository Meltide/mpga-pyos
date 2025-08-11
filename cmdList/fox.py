import os
from rich import print

from src.pyos.utils.man import ErrorCodeManager
from src.pyos.utils.config import *
from src.pyos.utils.foxShell import FoxShell

__doc__ = "FoxShell config"

__usage__ = {
    "theme [theme]": "Set theme for FoxShell",
    "theme list": "Show all themes",
    "reload": "Reload FoxShell",
}


def execute(self, args):
    global theme_list

    if not args:  # 检查是否提供了参数
        FoxShell.show_greeting(self)
        return

    theme_list = ["modern", "classic", "bash"]

    match args[0]:
        case "theme":
            if args[1] == "list":
                show_available_themes(self)
                return
            if len(args) < 2:
                raise SyntaxError("Please input a theme.")
                return
            elif args[1] not in theme_list:
                print(f"Unknown theme: {args[1]}")
                show_available_themes(self)
                self.error_code = ErrorCodeManager().get_code(SyntaxError)
                return
            self.fox["theme"] = args[1]
            with open(
                os.path.join("configs", "Users", self.username, "Fox", "fox_config.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(self.fox, f, ensure_ascii=False, indent=4)
                print(f"• [green]Theme set successfully.[/]")
        case "reload":
            FoxShell.reload(self)
        case _:
            print(f"Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)


def show_available_themes(self):
    print("Avaliable themes:")
    for theme in theme_list:
        if self.fox["theme"] == theme:
            print(f"- [blue]{theme} [/] (Current theme)")
            continue
        print(f"- [blue]{theme}[/]")
