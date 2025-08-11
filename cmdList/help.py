from src.pyos.utils.man import HelpManager

__doc__ = "Display help information for commands"

__usage__ = {
    "": "Show list of all commands",
    "[command]": "Show help for specific command",
}


def execute(self, args):
    helpman = HelpManager(self, args)

    if not helpman.args:
        helpman.show_all()
        return

    helpman.show_cmd()
    # 显示命令帮助信息
    helpman.show_info()
