import os, sys  # 系统库
from colorama import Fore  # 彩色文字库
from pyosLogin import Login
import traceback

from utils.man import ErrorCodeManager
from utils.config import SHOW_ERROR_DETAILS


class PyOS(Login):
    def __init__(self):
        super().__init__()
        # 初始化命令管理器
        if not hasattr(self, "command_manager"):
            raise AttributeError("CommandManager (command_manager) is not initialized in Login or PyOS.")

    def run(self, command_parts: list|tuple):
        """运行命令"""
        command_name = command_parts[0]

        if not command_name:  # 如果命令为空，直接返回
            return

        self.error_code = 0
        if len(command_parts) > 1 and command_parts[1] == '-h':  # 如果有帮助标志
            self._register_and_execute("help", [command_name])
        else:  # 执行命令（带参数或无参数）
            self._register_and_execute(command_name, command_parts[1:] if len(command_parts) > 1 else [])

    def _register_and_execute(self, command_name, args):
        """注册并执行命令"""
        self.command_manager.reg(command_name)
        self.command_manager.execute(args)  # 仅传递 args

if __name__ == "__main__":
    pyos=PyOS()
    try:
        pyos.login()
        '''except ModuleNotFoundError:
            os.system("pip install -r requirements.txt")'''
    except (SystemExit, KeyboardInterrupt, EOFError):
        pyos.fprint("You exited PyOS just now.",2)
    except (Exception, BaseException) as e:
        print(f"\nError: {Fore.RED}{type(e).__name__ if not str(e) else e}")
        print(f"Error code: {Fore.RED}{ErrorCodeManager().get_code(e)}")
        if SHOW_ERROR_DETAILS:
            print(f"Details: \n{traceback.format_exc()}")