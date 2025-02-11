from colorama import Fore #彩色文字库
import json #解析和保存json配置文件

__doc__="PyOS Host Manager"

def execute(self,args):
    self.error = 0
    print(f"{Fore.BLUE}PyOS Host Manager")
    print(f"Your hostname: {Fore.GREEN}{self.hostname}")
    print("Options:\n",
        "(1) Change your hostname\n",
        "(2) Exit")
    while True:
        self.hostcho = input("> ")
        if self.hostcho == "1":
            self.hostname = input("Type new hostname: ")
            with open("config.json", "r+", encoding="utf-8") as f:
                self.cfg["hostname"] = self.hostname
                json.dump(self.cfg,f,ensure_ascii=False,indent=4)
            print(f"{Fore.GREEN}Hostname change successfully.")
        elif self.hostcho == "2":
            break
        else:
            print(f"{Fore.RED}Unknown command.")
