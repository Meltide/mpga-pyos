import os, json
import datetime
from colorama import Fore, Back

from pyosInit import Init
from utils.man import ErrorCodeManager
from utils.config import *
from utils.err import *


class FoxShell(Init):
    def show_greeting(self):
        if self.SHOW_GREETING:
            try:
                with open(
                    os.path.join("configs", "Users", self.username, "Fox", "fox_greeting.txt"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    greeting_message = f.read()
            except FileNotFoundError:
                raise FileNotFoundError("Can't find fox_greeting.txt")
            except Exception:
                raise
            print(f"\n{greeting_message}")

    def reload(self):
        try:
            with open(
                os.path.join("configs", "Users", self.username, "Fox", "fox_config.json"), "r", encoding="utf-8"
            ) as f:
                fox = json.load(f)
            self.THEME = fox["theme"]
            self.SHOW_GREETING = fox["show_greeting"]
            print(f"• {Fore.GREEN}Reload successfully.")
        except Exception as e:
            raise RunningError(
                f"Can't reload FoxShell: {Fore.RED}{e if str(e) else type(e).__name__}"
            )

    def generate_prompt(self):
        """生成命令行提示符"""
        timestamp = datetime.datetime.now().strftime("%m/%d %H:%M:%S")
        match self.THEME:
            case "modern":
                return f"{f'{Back.RED}{Fore.WHITE} ✘ {self.error_code} ' if self.error_code else ''}{Back.WHITE}{Fore.BLACK} {timestamp} {Back.YELLOW} {self.username}@{self.hostname} {Back.BLUE}{Fore.WHITE} {self.current_directory} {Back.RESET}▶ "
            case "classic":
                return f"[{timestamp}] {Fore.GREEN}{self.username}{Fore.RESET}@{self.hostname} {Fore.BLUE}{self.current_directory}{Fore.RESET} {f'[{Fore.RED}{self.error_code}{Fore.RESET}]' if self.error_code else ''}> "
            case "bash":
                return f"{self.username}@{self.hostname}: {Fore.GREEN}{self.current_directory}{Fore.RESET} {f'[{Fore.RED}{self.error_code}{Fore.RESET}]' if self.error_code else ''}$ "
            case _:
                raise SyntaxError("Unknown theme.")

    @staticmethod
    def parse_commands(commands_str):
        commands = []
        command_parts = []
        buffer = ""
        inside_single_quote = False
        escaped = False

        for char in commands_str:
            if escaped:
                escaped = False
                if char == "'" or char == "\\" or char == ";":
                    buffer += char
            elif char == " " and not inside_single_quote:
                command_parts.append(buffer)
                buffer = ""
            elif char == "'":
                inside_single_quote = not inside_single_quote
            elif char == "\\":
                escaped = True
            elif char == ";" and not inside_single_quote:
                if buffer != "":
                    command_parts.append(buffer)
                    buffer = ""
                commands.append(command_parts)
                command_parts = []
            else:
                buffer += char

        if buffer != "":
            command_parts.append(buffer)
        if len(command_parts) > 0:
            commands.append(command_parts)

        return commands
