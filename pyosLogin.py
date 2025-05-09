import sys  # 系统库
from pyosInit import Init
import base64  # 加解密库
from colorama import Fore, Back, Style  # 彩色文字库
import time, datetime  # 时间日期库
import json  # 解析和保存json配置文件
import pwinput  # 密码隐藏库
import traceback

from utils.man import ErrorCodeManager
from utils.config import *
from utils.foxShell import FoxShell

class Login(Init):
    def __init__(self):
        super().__init__()
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

    def save_config(self):
        """保存配置到文件"""
        with open(os.path.join("configs", "profiles.json"), "r+", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False, indent=4)

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
            profiles["accounts"][new_username] = self.encode_password(new_password)
            self.save_config()
            self.fprint("Account created successfully.", 1)

    def reset_username(self):
        """重置用户名"""
        old_username = input("OldName: ")
        if self._validate_user(old_username):
            new_username = input("NewName: ")
            profiles["accounts"][new_username] = profiles["accounts"].pop(old_username)
            self.save_config()
            self.fprint("Username reset successfully.", 1)
        else:
            self.fprint("ERROR: Invalid username or password!", 3)

    def reset_password(self):
        """重置密码"""
        username = input("Name: ")
        if self._validate_user(username):
            new_password = pwinput.pwinput("NewPassword: ")
            profiles["accounts"][username] = self.encode_password(new_password)
            self.save_config()
            self.fprint("Password reset successfully.", 1)
        else:
            self.fprint("ERROR: Invalid username or password!", 3)

    def login_user(self):
        """用户登录"""
        stored_password = self.decode_password(profiles["accounts"][self.username])
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
            prompt = FoxShell.generate_prompt(self)
            command = input(prompt)
            try:
                self.run(command)
            except Exception as e:
                print(f"Error: {Fore.RED}{type(e).__name__ if not str(e) else e}")
                self.error_code = ErrorCodeManager().get_code(e)
                if SHOW_ERROR_DETAILS:
                    print(f"Details: \n{traceback.format_exc()}")

    def _validate_user(self, username):
        """验证用户名和密码"""
        if username in profiles["accounts"] and username != "root":
            stored_password = self.decode_password(profiles["accounts"][username])
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
        print("")
        if self.allow_system_commands:
            self.fprint("WARNING: Running system commands is enabled!", 2)