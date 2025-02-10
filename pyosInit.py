import json #解析和保存json配置文件
import random #随机库
import time #时间库
import os, sys #系统底层库
from colorama import init, Fore, Style #彩色文字库
import importlib

from cmdList.clear import execute as clear

class Init: #初始化
    def __init__(self):
        self.initCmd()
        init(autoreset=True)
        self.clsn = 0
        self.error = 0
        self.tips = ["You can find the default password in the passwd file.", "Maybe the coverter is useless :)", "'root' is the default user.", "Is this file system real?", "Columns make the calculator work."]
        with open('config.json','r',encoding='utf-8') as f: #读取配置
            self.cfg=json.load(f)
            self.names=self.cfg["accounts"].keys()
            self.hostname = self.cfg["hostname"]
            self.ver = "2.8"
            self.pyshver = "1.2.0"
            self.core = "20250203"
        time.sleep(0.5)
        clear(self)
        for i in range(1, 101):
            print("\r", end="")
            print(f"Starting: {i}%: ", "=" * (i // 8), end="", flush=True)
            # sys.stdout.flush()
            time.sleep(0.005)
        clear(self)
        self.printlist = [
            Style.DIM + "\nPY OS (R) Core Open Source System " + self.ver,
            Fore.BLUE
            + "  __  __ ___  ___   _   \n |  \\/  | _ \\/ __| /_\\  \n | |\\/| |  _/ (_ |/ _ \\ \n |_|  |_|_|  \\___/_/ \\_\\\n                        ",
            Fore.YELLOW + "Make PyOS Great Again!\n",
            "Tip: " + random.choice(self.tips),
            Fore.MAGENTA
            + "\nContributors: MeltIce, Yukari2024, EricDing618\nVisit this project in github: github.com/Meltide/mpga-pyos\nLifeinvader Studio Telegram Group: @MeetLifeinvader",
            Fore.CYAN
            + "\nAlso try PyOS's improved version by minqwq and bibimingming!\n",
        ]
        for i in self.printlist:
            print(i)
            time.sleep(0.1)
        self.count = 0
        self.file = "~"

    def initCmd(self):
        # 获取当前绝对路径
        currentPath = os.path.dirname(os.path.realpath(__file__))
        os.putenv("PYTHONPATH", currentPath)

        # 存储命令的文件夹
        cmdPath = os.path.join(currentPath, "cmdList")

        # 获取文件夹下所有命令
        cmdList = os.listdir(cmdPath)

        for cmd in cmdList:
            if os.path.splitext(cmd)[1] == ".py" and os.path.splitext(cmd)[0] != "registerCmd":
                importlib.import_module(f"cmdList.{os.path.splitext(cmd)[0]}", currentPath)