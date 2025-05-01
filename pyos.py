import random  # 随机库
from colorama import Fore  # 彩色文字库
from pyosLogin import login
import traceback


class PyOS(login):
    def run(self, cmds: str):
        """运行命令"""
        try:
            cmd = cmds.split(' ')
            cmdname = cmd[0]

            if not cmdname:  # 如果命令为空，直接返回
                return

            self.cmdman.reg(cmdname)
            self.error = 0

            if len(cmd) > 1:
                if cmd[1] == '-h':  # 如果有帮助标志
                    self.cmdman.reg("help")
                    self.cmdman.execute((self, [cmdname]))
                else:  # 执行带参数的命令
                    self.cmdman.execute((self, cmd[1:]))
            else:  # 执行无参数的命令
                self.cmdman.execute((self, []))

        except ImportError:
            self.fprint("Unknown command.", 3)
        except Exception as e:  # 捕获一般异常
            self.fprint(traceback.format_exc(), 3)


if __name__ == "__main__":
    PyOS()