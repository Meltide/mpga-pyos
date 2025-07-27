import base64  # 加解密库
from rich import print  # 彩色文字库
import json  # 解析和保存json配置文件
import pwinput  # 密码输入库
import os, shutil
from textwrap import dedent  # 格式化输出库
from ..src.pyos.utils.man import ErrorCodeManager
from ..src.pyos.utils.config import *

__doc__ = "PyOS User Manager"

__usage__ = {
    "log": "Show current login user",
    "list": "List all users",
    "create": "Create a new user",
    "delete [username]": "Delete a user",
    "change": "Change current user password",
    "auto [user/disable]": "Set auto login user",
}


def execute(self, args):
    if not args:  # 检查是否提供了参数
        print("Error: [red]No arguments provided. Please specify a valid command.[/]")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    match args[0]:
        case "log":
            print(f"Now login: [green]{self.username}[/]")
        case "list":
            show_all_users(self)
        case "create":
            create_user()
        case "delete":
            if not args[1]:
                raise SyntaxError("No username provided. Please input a username.")
            delete_user(args[1])
        case "change":
            change_passwd(self)
        case "auto":
            set_auto_login(args)
        case _:
            print(f"Error: [red]Unknown command '{args[0]}'[/].")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)


def show_all_users(self):
    print("All users:")
    for user in ACCOUNTS:
        if user == self.username:
            print(f"- [blue]{user} [/](Current user)")
            continue
        print(f"- [blue]{user}[/]")


def create_user():
    newname = input("Name: ")
    newgroup = input("Group: ")
    if newgroup not in GROUPS:
        raise NameError(f"Invaild group: '{newgroup}'")
    newpwd = pwinput.pwinput("Password: ")
    repwd = pwinput.pwinput("Re-enter Password: ")
    if newpwd != repwd:
        raise SyntaxError("The two passwords do not match!")
        return
    if newname in ACCOUNTS:
        print(f"[yellow]WARNING: The name was created![/]")
        return
    ACCOUNTS[newname] = {}
    ACCOUNTS[newname]["passwd"] = base64.b64encode(newpwd.encode("utf-8")).decode("utf-8")
    ACCOUNTS[newname]["group"] = newgroup
    with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    if not os.path.exists(os.path.join("configs", "Users", newname)):
        os.mkdir(os.path.join("configs", "Users", newname))
        for item in os.listdir(os.path.join("configs", "Users", "Template")):
            if os.path.isdir(os.path.join("configs", "Users", "Template", item)):
                shutil.copytree(os.path.join("configs", "Users", "Template", item), os.path.join("configs", "Users", newname, item))
            else:
                shutil.copy(os.path.join("configs", "Users", "Template", item), os.path.join("configs", "Users", newname, item))
    print(f"• [green]Created successfully.[/]")


def delete_user(username):
    global profiles, AUTO_LOGIN
    if len(ACCOUNT_NAMES) <= 1:
        raise SyntaxError("PyOS requires at least one user.")
    if username not in ACCOUNT_NAMES:
        raise NameError(f"Unknown username: '{username}'")
    if username == AUTO_LOGIN:
        profiles["auto_login"] = None
        AUTO_LOGIN = None
    
    del profiles["accounts"][username]
    if os.path.exists(os.path.join("configs", "Users", username)):
        shutil.rmtree(os.path.join("configs", "Users", username))
    
    with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    print(f"• [green]User '{username}' deleted successfully.[/]")


def change_passwd(self):
    stpasswd = base64.b64decode(profiles["accounts"][self.username]["passwd"].strip()).decode(
        "utf-8"
    )
    oldpwd = pwinput.pwinput("Old Password: ")
    reoldpwd = pwinput.pwinput("Re-enter Old Password: ")
    if oldpwd != reoldpwd:
        raise SyntaxError("The two passwords do not match!")
    if oldpwd == stpasswd:
        newpwd = pwinput.pwinput("New Password: ")
        ACCOUNTS[self.username]["passwd"] = base64.b64encode(newpwd.encode("utf-8")).decode(
            "utf-8"
        )
        with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False, indent=4)
        print(f"• [green]Resetted successfully.[/]")
    else:
        print(f"Error: [red]Invalid username or password![/]")


def set_auto_login(args):
    if len(args) < 2:
        print(f"Error: [red]Please input a username.[/]")
        return

    if args[1] == "disable":
        profiles["auto_login"] = None
        with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False, indent=4)
        print(f"• [green]Auto login disabled.[/]")
        return
    elif args[1] not in ACCOUNTS:
        print(f"Error: [red]Unknown user '{args[1]}'.[/]")
        return
    profiles["auto_login"] = args[1]
    with open(os.path.join("configs", "profiles.json"), "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    print(f"• [green]Auto login set to '{args[1]}'.[/]")
