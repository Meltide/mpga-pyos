from colorama import Fore, Back, Style
from utils.man import CommandManager
from utils.man import ErrorCodeManager

__doc__ = "Display help information for commands"

__usage__ = {
    "": "Show list of all commands",
    "<command>": "Show help for specific command"
}

def execute(self, args):
    cmdman = CommandManager(self)
    
    # 过滤和清理参数，只保留字符串类型的有效命令名
    clean_args = []
    for arg in args:
        if isinstance(arg, str) and arg.isidentifier():
            clean_args.append(arg)
    
    # 无参数时显示所有命令
    if not clean_args:
        print(f"Available Commands:{Style.RESET_ALL}")
        for category, cmds in cmdman.allcmds.items():
            print(f"{Back.BLUE} {category} ")
            for cmd in sorted(cmds):
                cmdman.reg(cmd)
                try:
                    doc = cmdman.getpkg().__doc__ or "No description"
                    print(f"{cmd:<15}{Style.RESET_ALL} {doc}")
                except ImportError:
                    print(f"{cmd:<15}{Style.RESET_ALL} (Not loadable)")
        return

    # 获取要查询的命令名（第一个有效参数）
    cmd_name = clean_args[0]
    cmdman.reg(cmd_name)
    
    # 检查命令是否存在
    if not cmdman.loaded_cmd():
        print(f"{Fore.RED}Error: Command '{cmd_name}' not found{Style.RESET_ALL}")
        print(f"Type 'help' to see available commands")
        self.error_code = ErrorCodeManager().get_code(FileNotFoundError)
        return

    # 显示命令帮助信息
    try:
        pkg = cmdman.getpkg()
        print(f"\n{Back.BLUE} Help for: {cmd_name} {Style.RESET_ALL}")
        
        # 显示描述
        description = getattr(pkg, '__doc__', "No description available")
        print(f"\n{description}\n")
        
        # 显示用法
        if hasattr(pkg, '__usage__'):
            print(f"{Back.BLUE} Usage Examples: {Style.RESET_ALL}")
            for usage, desc in pkg.__usage__.items():
                print(f"  {cmd_name} {Fore.GREEN}{usage:<15}{Style.RESET_ALL} {desc}")
        else:
            print(f"{Fore.YELLOW}No usage examples available{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Error loading command help: {str(e)}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)