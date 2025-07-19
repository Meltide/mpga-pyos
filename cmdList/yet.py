import json, shutil, os, importlib
import zipfile
import subprocess
import sys

from utils.config import *
from utils.yet import *
from utils.man import ErrorCodeManager, CommandManager
from utils.err import RunningError
from rich import print

__doc__ = "YET Package manager"  # 第三方命令注册模块

__usage__ = {
    "install [path]": "Install a local app",
    "remove [command]": "Remove apps",
    "list": "List all third-party apps",
    "info [command]": "Show package information",
}

def execute(self, args):
    """主执行函数"""
    if not args:
        print(
            f"Error: [red]No arguments provided. Please specify a valid command.[/]"
        )
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    match args[0]:
        case "install":
            install(self, args)
            auto_reload_commands(self)  # 安装后自动重载
        case "remove":
            remove_app(self, args)
            auto_reload_commands(self)  # 移除后自动重载
        case "list":
            list_apps(self, args)
        case "info":
            show_package_info(self, args)
        case _:
            print(f"Error: [red]Unknown command '{args[0]}'.[/]")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)
