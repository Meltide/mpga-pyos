import json  # 解析和保存json配置文件
import random  # 随机库
import time  # 时间库
import sys  # 系统库
from colorama import init, Fore, Style  # 彩色文字库
from art import text2art  # 艺术字库

from cmdList.clear import execute as clear
from man import CommandManager


class Init:  # 初始化
    def __init__(self):
        init(autoreset=True)
        self.command_manager = CommandManager(self, self)  # 命令管理器
        self.clear_screen_count = 0  # 清屏计数
        self.error_code = 0  # 错误代码
        self.tips_list = [  # 提示列表
            "You can find the default password in the passwd file.",
            "Maybe the coverter is useless :)",
            "'root' is the default user.",
            "Is this file system real?",
            "Columns make the calculator work."
        ]
        self.selected_tip = random.choice(self.tips_list)  # 随机选择提示
        self.color_modes = [Fore.WHITE, Fore.GREEN, Fore.YELLOW, Fore.RED]  # 颜色模式列表

        # 加载配置
        self._load_config()

        # 显示启动进度条
        time.sleep(0.5)
        clear(self, [])
        self._show_progress_bar()
        clear(self, [])

        # 打印启动信息
        self._print_startup_messages()

        self.command_count = 0  # 命令计数
        self.current_directory = "~"  # 当前目录

    def _load_config(self):
        """加载配置文件"""
        with open("config.json", "r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)
            self.account_names = self.config["accounts"].keys()  # 账户名称
            self.hostname = self.config["hostname"]  # 主机名
            self.allow_system_commands = self.config["os.system"]  # 是否支持运行系统命令
            self.version = "2.9"  # 系统版本
            self.shell_version = "1.2.0"  # Shell 版本
            self.core_version = "20250405"  # 核心版本

    def _show_progress_bar(self):
        """显示启动进度条"""
        for progress in range(1, 101):
            sys.stdout.write(f"\rStarting: {progress}%: {'=' * (progress // 8)}")
            sys.stdout.flush()
            time.sleep(0.005)
        print()  # 换行

    def _print_startup_messages(self):
        """打印启动信息"""
        startup_messages = [
            Style.DIM + f"\nMPGA PyOS Open Source System {self.version}",
            Fore.BLUE + text2art("MPGA", font="small"),
            Fore.YELLOW + "Make PyOS Great Again!\n",
            f"Tip: {self.selected_tip}",
            Fore.MAGENTA
            + "\nContributors: MeltIce, Yukari2024, EricDing618\n"
            + "Visit this project in github: github.com/Meltide/mpga-pyos\n"
            + "MPGA Team Telegram Group: @MPGATeam\n"
            + "MPGA Team Matrix Group: #MPGATeam:mozilla.org",
            Fore.CYAN
            + "\nAlso try PyOS's improved version by minqwq and bibimingming!\n",
        ]
        for message in startup_messages:
            print(message)
            time.sleep(0.1)

    def fprint(self, message, mode=0):
        """打印消息
        mode: 0白色，1绿色，2黄色，3红色
        """
        print(self.color_modes[mode] + message)
        if mode == 3:
            self.error_code = random.randint(100, 999)