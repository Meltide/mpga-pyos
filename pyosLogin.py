from pyosInit import Init
import base64 #加解密库
from colorama import Fore, Back, Style #彩色文字库
import time,datetime #时间日期库
import json #解析和保存json配置文件
import pwinput #密码隐藏库
import random #随机库

class login(Init):
    def __init__(self):
        super().__init__()
        try:
            times = datetime.datetime.now()
            while self.count < 3:
                self.user = input(f"{self.hostname} login: ")
                if self.user=="create": #可新建账户
                    newname=input('Name: ')
                    newpwd=pwinput.pwinput()
                    if newname in self.names:
                        self.fprint("WARNING: The name was created!",2)
                    elif newname in ("create","reset name","reset pwd"): #防止卡出bug
                        self.fprint("Invalid username!",3)
                    else:
                        self.cfg["accounts"][newname]=base64.b64encode(newpwd.encode("utf-8")).decode("utf-8")
                        with open("config.json","r+",encoding="utf-8") as f:
                            json.dump(self.cfg,f,ensure_ascii=False,indent=4)
                        self.fprint('Created successfully.',1)
                elif self.user=="reset name": #重置用户名
                    oldname=input('OldName: ')
                    stpasswd = base64.b64decode(self.cfg["accounts"][oldname].strip()).decode("utf-8")
                    pwd=pwinput.pwinput()
                    if pwd==stpasswd and oldname in self.cfg["accounts"].keys() and oldname!="root":
                        newname=input("NewName: ")
                        del self.cfg["accounts"][oldname]
                        self.cfg["accounts"][newname]=base64.b64encode(pwd.encode("utf-8")).decode("utf-8")
                        with open("config.json","r+",encoding="utf-8") as f:
                            json.dump(self.cfg,f,ensure_ascii=False,indent=4)
                        self.fprint('Resetted successfully.',1)
                    else:
                        self.fprint("ERROR: Invalid username or password!",3)
                elif self.user=="reset pwd": #重置密码
                    name=input('Name: ')
                    stpasswd = base64.b64decode(self.cfg["accounts"][name].strip()).decode("utf-8")
                    oldpwd=pwinput.pwinput("OldPassword: ")
                    if oldpwd==stpasswd and oldname in self.cfg["accounts"].keys() and oldname!="root":
                        newpwd=pwinput.pwinput("NewPassword: ")
                        self.cfg["accounts"][name]=base64.b64encode(newpwd.encode("utf-8")).decode("utf-8")
                        with open("config.json","r+",encoding="utf-8") as f:
                            json.dump(self.cfg,f,ensure_ascii=False,indent=4)
                        print(f'{Fore.GREEN}Resetted successfully.')
                    else:
                        print(f"{Fore.RED}ERROR: Invalid username or password!")
                elif self.user in self.names: #正常登录
                    stpasswd = base64.b64decode(self.cfg["accounts"][self.user].strip()).decode("utf-8")
                    while self.count < 3:
                        passwd = pwinput.pwinput()
                        if passwd == stpasswd:
                            print("Last login: "+ Fore.CYAN+ times.strftime("%y/%m/%d %H:%M:%S"))
                            time.sleep(0.45)
                            print("")
                            if self.runsys:
                                self.fprint("WARNING: Running system commands is enabled!",2)
                            while self.count < 3:
                                zshp9k_tm = datetime.datetime.now()
                                zshp9k_pre = zshp9k_tm.strftime(" %m/%d %H:%M:%S ")
                                zshp9k = zshp9k_pre
                                if self.errcode:
                                    self.cmd = input(f"{Back.RED}{Fore.WHITE} ✘ {self.errcode} {Back.WHITE}{Fore.BLACK}{zshp9k}{Back.YELLOW} {self.user}@{self.hostname} {Back.BLUE}{Fore.WHITE} {self.file} {Back.RESET}> ")
                                else:
                                    self.cmd = input(f"{Back.WHITE}{Fore.BLACK}{zshp9k}{Back.YELLOW} {self.user}@{self.hostname} {Back.BLUE}{Fore.WHITE} {self.file} {Back.RESET}> ")
                                self.run(self.cmd)
                        elif passwd == "":
                            print(f"{Style.DIM}Tip: You can find the default password in the passwd file.")
                        else:
                            print("Error password! Please retry")
                            print(f"{Style.DIM}Tip: You can find the default password in the passwd file.")
                else:
                    print("Invalid user! Please retry")
                    print(Style.DIM + "Tip: 'root' is the default user.")
        except (KeyboardInterrupt,EOFError):
            self.fprint("\nYou exited PyOS just now!",3)
            quit(114)