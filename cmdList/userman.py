import base64  # 加解密库
from colorama import Fore  # 彩色文字库
import json  # 解析和保存json配置文件
import pwinput  # 密码输入库
from textwrap import dedent  # 格式化输出库

__doc__ = "PyOS User Manager"

__usage__ = {
    "log": "Show current login user",
    "create": "Create a new user",
    "change": "Change current user password"
}

def execute(self, args):
    if not args:  # 检查是否提供了参数
        print(f"Error: {Fore.RED}No arguments provided. Please specify a valid command.")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        return

    match args[0]:
        case "log":
            print(f"Now login: {Fore.GREEN}{self.username}")
        case "create":
            newname = input('Name: ')
            newpwd = pwinput.pwinput()
            if newname in self.names:
                print(f"{Fore.YELLOW}WARNING: The name was created!")
                return
            self.config["accounts"][newname] = base64.b64encode(newpwd.encode("utf-8")).decode("utf-8")
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            print(f'{Fore.GREEN}Created successfully.')
        case "change":
            stpasswd = base64.b64decode(self.config["accounts"][self.username].strip()).decode("utf-8")
            oldpwd = pwinput.pwinput("Old Password: ")
            if oldpwd == stpasswd:
                newpwd = pwinput.pwinput("New Password: ")
                self.config["accounts"][self.username] = base64.b64encode(newpwd.encode("utf-8")).decode("utf-8")
                with open("config.json", "r+", encoding="utf-8") as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=4)
                print(f'{Fore.GREEN}Resetted successfully.')
            else:
                print(f"Error: {Fore.RED}Invalid username or password!")
        case _:
            print(f"Error: {Fore.RED}Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")