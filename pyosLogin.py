import sys  # 系统库
from pyosInit import Init
import base64  # 加解密库
from colorama import Fore, Back, Style  # 彩色文字库
import time, datetime  # 时间日期库
import json  # 解析和保存json配置文件
import pwinput  # 密码隐藏库


class Login(Init):
    def __init__(self):
        super().__init__()
        try:
            self.current_time = datetime.datetime.now()
            self.max_attempts = 3
            while self.command_count < self.max_attempts:
                self.username = input(f"{self.hostname} login: ")
                if self.username == "create":
                    self.create_account()
                elif self.username == "reset name":
                    self.reset_username()
                elif self.username == "reset pwd":
                    self.reset_password()
                elif self.username in self.account_names:
                    self.login_user()
                else:
                    self._invalid_user_message()
        except (KeyboardInterrupt, EOFError):
            self.fprint("\nYou exited PyOS just now!", 3)
            sys.exit(114)  # 使用 sys.exit() 优雅退出程序

    def save_config(self):
        """保存配置到文件"""
        with open("config.json", "r+", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def encode_password(self, password):
        """加密密码"""
        return base64.b64encode(password.encode("utf-8")).decode("utf-8")

    def decode_password(self, encoded_password):
        """解密密码"""
        return base64.b64decode(encoded_password.strip()).decode("utf-8")

    def create_account(self):
        """创建新账户"""
        new_username = input("Name: ")
        new_password = pwinput.pwinput()
        if new_username in self.account_names:
            self.fprint("WARNING: The name already exists!", 2)
        elif new_username in ("create", "reset name", "reset pwd"):
            self.fprint("Invalid username!", 3)
        else:
            self.config["accounts"][new_username] = self.encode_password(new_password)
            self.save_config()
            self.fprint("Account created successfully.", 1)

    def reset_username(self):
        """重置用户名"""
        old_username = input("OldName: ")
        if self._validate_user(old_username):
            new_username = input("NewName: ")
            self.config["accounts"][new_username] = self.config["accounts"].pop(old_username)
            self.save_config()
            self.fprint("Username reset successfully.", 1)
        else:
            self.fprint("ERROR: Invalid username or password!", 3)

    def reset_password(self):
        """重置密码"""
        username = input("Name: ")
        if self._validate_user(username):
            new_password = pwinput.pwinput("NewPassword: ")
            self.config["accounts"][username] = self.encode_password(new_password)
            self.save_config()
            self.fprint("Password reset successfully.", 1)
        else:
            self.fprint("ERROR: Invalid username or password!", 3)

    def login_user(self):
        """用户登录"""
        stored_password = self.decode_password(self.config["accounts"][self.username])
        while self.command_count < self.max_attempts:
            entered_password = pwinput.pwinput()
            if entered_password == stored_password:
                self._successful_login_message()
                self.start_shell()
                break
            else:
                self._invalid_password_message()

    def start_shell(self):
        """启动命令行交互"""
        while self.command_count < self.max_attempts:
            timestamp = datetime.datetime.now().strftime(" %m/%d %H:%M:%S ")
            prompt = self._generate_prompt(timestamp)
            command = input(prompt)
            self.run(command)

    def _validate_user(self, username):
        """验证用户名和密码"""
        if username in self.config["accounts"] and username != "root":
            stored_password = self.decode_password(self.config["accounts"][username])
            entered_password = pwinput.pwinput("Password: ")
            return entered_password == stored_password
        return False

    def _invalid_user_message(self):
        """打印无效用户提示"""
        self.fprint("Invalid user! Please retry", 3)
        print(Style.DIM + "Tip: 'root' is the default user.")

    def _invalid_password_message(self):
        """打印无效密码提示"""
        self.fprint("Error password! Please retry", 3)
        print(f"{Style.DIM}Tip: You can find the default password in the passwd file.")

    def _successful_login_message(self):
        """打印成功登录提示"""
        print("Last login: " + Fore.CYAN + self.current_time.strftime("%y/%m/%d %H:%M:%S"))
        time.sleep(0.45)
        print("")
        if self.allow_system_commands:
            self.fprint("WARNING: Running system commands is enabled!", 2)

    def _generate_prompt(self, timestamp):
        """生成命令行提示符"""
        if self.error_code:
            return (
                f"{Back.RED}{Fore.WHITE} ✘ {self.error_code} {Back.WHITE}{Fore.BLACK}{timestamp}"
                f"{Back.YELLOW} {self.username}@{self.hostname} {Back.BLUE}{Fore.WHITE} {self.current_directory} {Back.RESET}> "
            )
        return (
            f"{Back.WHITE}{Fore.BLACK}{timestamp}{Back.YELLOW} {self.username}@{self.hostname} "
            f"{Back.BLUE}{Fore.WHITE} {self.current_directory} {Back.RESET}> "
        )