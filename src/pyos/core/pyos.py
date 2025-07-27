import traceback  # 异常追踪库
import sys

from pathlib import Path  # 路径处理库
from rich import print  # 彩色文字库
'''for i in range(3):
    sys.path.append(Path(__file__).parents[i])
print(Path(__file__).parents[1])'''

from .login import Login
'''for path in PathEnum:
    print(path.name,path.value)
    sys.path.append(path.value)
'''
from ..utils.foxShell import FoxShell
from ..utils.man import ErrorCodeManager
from ..utils.config import SHOW_BASE_ERROR_DETAILS


class PyOS(Login):
    def __init__(self,debug=False):
        super().__init__()
        # 初始化命令管理器
        if not hasattr(self, "command_manager"):
            raise AttributeError(
                "CommandManager (command_manager) is not initialized in Login or PyOS."
            )
        if not debug: #为方便调试pyoscript，可以设置debug参数，不启动登录界面
            self.init_cli()

    def run(self, commands: str):
        """运行命令"""
        commands = FoxShell.parse_commands(commands)

        for command_parts in commands:
            if len(command_parts) < 1:
                continue

            command_name = command_parts[0]
            if not command_name:  # 如果命令为空，直接返回
                continue

            self.error_code = 0
            try:
                if (
                    len(command_parts) > 1 and command_parts[1] == "-h"
                ):  # 如果有帮助标志
                    self._register_and_execute("help", [command_name])
                else:  # 执行命令（带参数或无参数）
                    self._register_and_execute(
                        command_name,
                        command_parts[1:] if len(command_parts) > 1 else [],
                    )
            except FileNotFoundError:
                raise FileNotFoundError("Unknown command: " + "".join(command_parts))

    def _register_and_execute(self, command_name, args):
        """注册并执行命令"""
        self.command_manager.reg(command_name)
        self.command_manager.execute(self.username, args)  # 仅传递 args


if __name__ == "__main__":
    try:
        PyOS()
    except (KeyboardInterrupt, EOFError) as e:
        if isinstance(e, EOFError):
            print()
        print("\n[red]You exited PyOS just now.[/]")
    except SystemExit:
        pass
    except (Exception, BaseException) as e:
        print(f"\nError: [red]{type(e).__name__ if not str(e) else e}[/]")
        print(f"Error code: [red]{ErrorCodeManager().get_code(e)}[/]")
        if SHOW_BASE_ERROR_DETAILS:
            print(f"Details: \n{traceback.format_exc()}")
