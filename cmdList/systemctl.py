import json
from rich import print
from utils.config import *
from utils.man import ErrorCodeManager

__doc__ = "Set system policy"

__usage__ = {
    "enable [policy]": "Enable policys",
    "disable [policy]": "Disable policys",
    "list": "Show all policys",
}


def execute(self, args):
    if not args:  # 检查是否提供了参数
        print(
            f"Error: [red]No arguments provided. Please specify a valid command.[/]"
        )
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
                print(f"- [blue]{policy}[/]: [yellow]{status}[/]")
        case _:
            print(f"Error: [red]Unknown command '{args[0]}'.[/]")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)


def set_status(self, status, args):
    if not args:
        raise SyntaxError("No settings inputed.")
        return
    elif args[0] not in policys:
        raise SyntaxError(f"Unknown policy '{args[0]}'")

    try:
        with open(os.path.join("configs", "system_policys.json"), "w", encoding="utf-8") as f:
            policys[args[0]] = status
            json.dump(policys, f, ensure_ascii=False, indent=4)
            print(f"The new status of [blue]{args[0]}[/]: [yellow]{status}[/]")
            print("It will take effect after restarting the system.")
    except Exception as e:
        print(f"Error: [red]{e}[/]")
        self.error_code = ErrorCodeManager.get_code(e)
