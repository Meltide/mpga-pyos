import os  # 系统库
from colorama import Fore  # 彩色文字库
from pyosLogin import Login
import traceback


class PyOS(Login):
    def __init__(self):
        super().__init__()
        # 初始化命令管理器
        if not hasattr(self, "command_manager"):
            raise AttributeError("CommandManager (command_manager) is not initialized in Login or PyOS.")

    def run(self, commands: str):
        """运行命令"""
        try:
            command_parts = commands.split(' ')
            command_name = command_parts[0]

            if not command_name:  # 如果命令为空，直接返回
                return

            self.error_code = 0
            if len(command_parts) > 1 and command_parts[1] == '-h':  # 如果有帮助标志
                self._register_and_execute("help", [command_name])
            else:  # 执行命令（带参数或无参数）
                self._register_and_execute(command_name, command_parts[1:] if len(command_parts) > 1 else [])

        except ImportError:
            self.fprint("Unknown command.", 3)
        except IndexError:
            self.fprint("Invalid command format. Please check your input.", 3)
        except Exception as e:  # 捕获一般异常
            self.fprint(f"An error occurred:\n{traceback.format_exc()}", 3)

    def _register_and_execute(self, command_name, args):
        """注册并执行命令"""
        try:
            self.command_manager.reg(command_name)
            self.command_manager.execute((self, args))
        except Exception as e:
            self.fprint(f"Failed to execute command '{command_name}': {e}", 3)


if __name__ == "__main__":
    try:
        PyOS()
    except ModuleNotFoundError:
        os.system("pip install -r requirements.txt")
    except Exception as e:
        print(f"Failed to start PyOS: {e}")