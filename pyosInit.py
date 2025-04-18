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
        self.cmdman = CommandManager(self, self)
        self.clsn = 0
        self.errcode = 0
        self.tips = [
            "You can find the default password in the passwd file.",
            "Maybe the coverter is useless :)",
            "'root' is the default user.",
            "Is this file system real?",
            "Columns make the calculator work.",
        ]
        self.selected_tip = random.choice(self.tips)  # 提前选择随机提示
        self.color_modes = [Fore.WHITE, Fore.GREEN, Fore.YELLOW, Fore.RED]  # 颜色模式列表

        # 读取配置
        with open("config.json", "r", encoding="utf-8") as f:
            self.cfg = json.load(f)
            self.names = self.cfg["accounts"].keys()
            self.hostname = self.cfg["hostname"]
            self.runsys = self.cfg["os.system"]  # 是否支持运行系统命令
            self.ver = "2.8"
            self.pyshver = "1.2.0"
            self.core = "20250405"

        time.sleep(0.5)
        clear(self, [])
        self._show_progress_bar()
        clear(self, [])

        # 打印启动信息
        self.printlist = [
            Style.DIM + f"\nMPGA PyOS Open Source System {self.ver}",
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
        for line in self.printlist:
            print(line)
            time.sleep(0.1)

        self.count = 0
        self.file = "~"

    def _show_progress_bar(self):
        """显示启动进度条"""
        for i in range(1, 101):
            sys.stdout.write(f"\rStarting: {i}%: {'=' * (i // 8)}")
            sys.stdout.flush()
            time.sleep(0.005)
        print()  # 换行

    def fprint(self, msg, mode=0):
        """打印消息
        mode: 0白色，1绿色，2黄色，3红色
        """
        print(self.color_modes[mode] + msg)
        if mode == 3:
            self.errcode = random.randint(100, 999)