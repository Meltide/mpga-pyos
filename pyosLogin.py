from pyosInit import Init
import base64  # 加解密库
from colorama import Fore, Back, Style  # 彩色文字库
import time, datetime  # 时间日期库
import json  # 解析和保存json配置文件
import pwinput  # 密码隐藏库


class login(Init):
    def __init__(self):
        super().__init__()
        try:
            self.times = datetime.datetime.now()
            while self.count < 3:
                self.user = input(f"{self.hostname} login: ")
                if self.user == "create":
                    self.create_account()
                elif self.user == "reset name":
                    self.reset_username()
                elif self.user == "reset pwd":
                    self.reset_password()
                elif self.user in self.names:
                    self.login_user()
                else:
                    self.fprint("Invalid user! Please retry", 3)
                    print(Style.DIM + "Tip: 'root' is the default user.")
        except (KeyboardInterrupt, EOFError):
            self.fprint("\nYou exited PyOS just now!", 3)
            self.count=114514

    def save_config(self):
        """保存配置到文件"""
        with open("config.json", "r+", encoding="utf-8") as f:
            json.dump(self.cfg, f, ensure_ascii=False, indent=4)

    def encode_password(self, password):
        """加密密码"""
        return base64.b64encode(password.encode("utf-8")).decode("utf-8")

    def decode_password(self, encoded_password):
        """解密密码"""
        return base64.b64decode(encoded_password.strip()).decode("utf-8")

    def create_account(self):
        """创建新账户"""
        newname = input("Name: ")
        newpwd = pwinput.pwinput()
        if newname in self.names:
            self.fprint("WARNING: The name was created!", 2)
        elif newname in ("create", "reset name", "reset pwd"):
            self.fprint("Invalid username!", 3)
        else:
            self.cfg["accounts"][newname] = self.encode_password(newpwd)
            self.save_config()
            self.fprint("Created successfully.", 1)

    def reset_username(self):
        """重置用户名"""
        oldname = input("OldName: ")
        if oldname in self.cfg["accounts"].keys() and oldname != "root":
            stpasswd = self.decode_password(self.cfg["accounts"][oldname])
            pwd = pwinput.pwinput()
            if pwd == stpasswd:
                newname = input("NewName: ")
                del self.cfg["accounts"][oldname]
                self.cfg["accounts"][newname] = self.encode_password(pwd)
                self.save_config()
                self.fprint("Resetted successfully.", 1)
            else:
                self.fprint("ERROR: Invalid username or password!", 3)
        else:
            self.fprint("ERROR: Invalid username or password!", 3)

    def reset_password(self):
        """重置密码"""
        name = input("Name: ")
        if name in self.cfg["accounts"].keys() and name != "root":
            stpasswd = self.decode_password(self.cfg["accounts"][name])
            oldpwd = pwinput.pwinput("OldPassword: ")
            if oldpwd == stpasswd:
                newpwd = pwinput.pwinput("NewPassword: ")
                self.cfg["accounts"][name] = self.encode_password(newpwd)
                self.save_config()
                self.fprint("Resetted successfully.", 1)
            else:
                self.fprint("ERROR: Invalid username or password!", 3)
        else:
            self.fprint("ERROR: Invalid username or password!", 3)

    def login_user(self):
        """用户登录"""
        stpasswd = self.decode_password(self.cfg["accounts"][self.user])
        while self.count < 3:
            passwd = pwinput.pwinput()
            if passwd == stpasswd:
                print("Last login: " + Fore.CYAN + self.times.strftime("%y/%m/%d %H:%M:%S"))
                time.sleep(0.45)
                print("")
                if self.runsys:
                    self.fprint("WARNING: Running system commands is enabled!", 2)
                self.start_shell()
                break
            elif passwd == "":
                print(f"{Style.DIM}Tip: You can find the default password in the passwd file.")
            else:
                self.fprint("Error password! Please retry", 3)
                print(f"{Style.DIM}Tip: You can find the default password in the passwd file.")

    def start_shell(self):
        """启动命令行交互"""
        while self.count < 3:
            zshp9k_tm = datetime.datetime.now()
            zshp9k_pre = zshp9k_tm.strftime(" %m/%d %H:%M:%S ")
            zshp9k = zshp9k_pre
            if self.errcode:
                self.cmd = input(
                    f"{Back.RED}{Fore.WHITE} ✘ {self.errcode} {Back.WHITE}{Fore.BLACK}{zshp9k}{Back.YELLOW} {self.user}@{self.hostname} {Back.BLUE}{Fore.WHITE} {self.file} {Back.RESET}> "
                )
            else:
                self.cmd = input(
                    f"{Back.WHITE}{Fore.BLACK}{zshp9k}{Back.YELLOW} {self.user}@{self.hostname} {Back.BLUE}{Fore.WHITE} {self.file} {Back.RESET}> "
                )
            self.run(self.cmd)
