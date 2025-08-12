import json  # 解析和保存json配置文件
import random  # 随机库
import time  # 时间库
import sys  # 系统库
from rich import print  # 彩色文字库
from rich.markup import escape
from art import text2art  # 艺术字库
from enum import Enum
from pathlib import Path  # 路径处理库

from cmdList.clear import execute as clear
from ..utils.man import CommandManager
from ..utils.config import *


class Init:  # 初始化
    def __init__(self):
        self.command_manager = CommandManager(self, "")  # 命令管理器
        self.error_code = 0  # 错误代码
        self.hostname = HOSTNAME
        
        self.username = "root"  # 默认用户名
        self.version = "3.2 Corgi"  # 系统版本
        self.shell_version = "1.0"  # Shell 版本
        self.core_version = "20250517"  # 核心版本
    def init_cli(self):  
        self.tips_list = [  # 提示列表
            "You can find the default password in the passwd file.",
            "Maybe the coverter is useless :)",
            "'root' is the default user.",
            "Is this file system real?",
            "Columns make the calculator work.",
        ]
        self.selected_tip = random.choice(self.tips_list)  # 随机选择提示
        
        self.color_modes = [
            '[white]',
            '[green]',
            '[yellow]',
            '[red]',
        ]  # 颜色模式列表

        clear(self, [])

        # 打印启动信息
        self._print_startup_messages()

        self.command_count = 0  # 命令计数
        self.current_directory = "~"  # 当前目录

    def _print_startup_messages(self):
        """打印启动信息"""
        startup_messages = [
            f"\nMPGA PyOS Open Source System [default not bold]{self.version}[/]",
            '[blue]' + text2art("MPGA", font="small")+'[/]',
            f"[yellow]Make PyOS Great Again![/]\n",
            f"Tip: {self.selected_tip}",
            (
                f"[cyan]\nAlso try PyOS's improved version by minqwq and bibimingming![/]\n"
                if SHOW_AD
                else ""
            ),
        ]

        if USE_CUSTOM_STARTUPMSG:
            try:
                with open(
                    os.path.join("configs", "PyOS", "startup_msg.txt"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    startup_messages = f.readlines()
            except FileNotFoundError:
                print(f"Error: [red]Can't find startup_msg.txt[/]")
                return

        for message in startup_messages:
            print(message.strip() if USE_CUSTOM_STARTUPMSG else message)
            time.sleep(0.05)
        if USE_CUSTOM_STARTUPMSG:
            print()

    def fprint(self, message, mode=0):
        """打印消息
        mode: 0白色，1绿色，2黄色，3红色
        """
        print(self.color_modes[mode] + message+'[/]')
        if mode == 3:
            random.seed(time.time_ns())  # 避免错误代码一致
            self.errcode = random.randint(100, 999)
