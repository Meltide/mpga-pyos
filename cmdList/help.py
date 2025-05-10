from colorama import Fore, Back, Style
from utils.man import HelpManager
from utils.man import ErrorCodeManager

__doc__ = "Display help information for commands"

__usage__ = {
    "": "Show list of all commands",
    "<command>": "Show help for specific command"
}

def execute(self, args):
    helpman = HelpManager(self, args)
    
  # 无参数时显示所有命令
    if not helpman.args:
        helpman.show_all()
        return

    helpman.show_cmd()
    # 显示命令帮助信息
    helpman.show_info()