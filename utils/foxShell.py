import os, json
import datetime
from colorama import Fore, Back

from pyosInit import Init
from utils.config import *

class FoxShell(Init):
    def generate_prompt(self):
        """生成命令行提示符"""
        timestamp = datetime.datetime.now().strftime("%m/%d %H:%M:%S")
        match THEME:
            case "modern":
                return (
                    f"{f'{Back.RED}{Fore.WHITE} ✘ {self.error_code} ' if self.error_code else ''}{Back.WHITE}{Fore.BLACK} {timestamp} {Back.YELLOW} {self.username}@{self.hostname} {Back.BLUE}{Fore.WHITE} {self.current_directory} {Back.RESET}▶ "
                )
            case "classic":
                return (
                    f"[{timestamp}] {Fore.GREEN}{self.username}{Fore.RESET}@{self.hostname} {Fore.BLUE}{self.current_directory}{Fore.RESET} {f'[{Fore.RED}{self.error_code}{Fore.RESET}]' if self.error_code else ''}> "
                )