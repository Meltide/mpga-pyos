import json #解析和保存json配置文件
import random #随机库
import time #时间库
from colorama import init, Fore, Style #彩色文字库
from art import text2art #艺术字库

from cmdList.clear import execute as clear
from cmd_manager import CommandManager

class Init: #初始化
    def __init__(self):
        init(autoreset=True)
        self.cmdman = CommandManager(self,self)
        self.clsn = 0
        self.errcode = 0
        self.tips = ["You can find the default password in the passwd file.", "Maybe the coverter is useless :)", "'root' is the default user.", "Is this file system real?", "Columns make the calculator work."]
        with open('config.json','r',encoding='utf-8') as f: #读取配置
            self.cfg=json.load(f)
            self.names=self.cfg["accounts"].keys()
            self.hostname = self.cfg["hostname"]
            self.ver = "2.8"
            self.pyshver = "1.2.0"
            self.core = "20250405"
        time.sleep(0.5)
        clear(self,[])
        for i in range(1, 101):
            print("\r", end="")
            print(f"Starting: {i}%: ", "=" * (i // 8), end="", flush=True)
            # sys.stdout.flush()
            time.sleep(0.005)
        clear(self,[])
        self.printlist = [
            Style.DIM + "\nPY OS (R) Core Open Source System " + self.ver,
            Fore.BLUE + text2art("MPGA", font="small"),
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
    
    def fprint(self,msg,mode=0):
        '''mode:0白色，1绿色，2黄色，3红色'''
        modelist=[Fore.WHITE,Fore.GREEN,Fore.YELLOW,Fore.RED]
        print(modelist[mode]+msg)
        if mode==3:
            self.errcode = random.randint(100, 999)