import json, shutil, os, importlib
from utils.config import cfg
from . import help, sysname
from utils.man import ErrorCodeManager
from utils.man import CommandManager
from colorama import Fore, Back, Style

__doc__ = "YET Package manager"  # 第三方命令注册模块

__usage__ = {
    "install": "Install apps online",
    "install-local": "Add a local app",
    "remove": "Remove apps",
    "list": "List all third-party apps"
}

def execute(self, args):
    """主执行函数"""
    if not args:
        print(f"Error: {Fore.RED}No arguments provided. Please specify a valid command.")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        return
    
    match args[0]:
        case "install":
            install_online(self, args)
        case "install-local":
            install_local(self, args)
        case "remove":
            remove_app(self, args)
        case "list":
            list_apps(self, args)
        case _:
            print(f"Error: {Fore.RED}Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")

def install_online(self, args):
    """在线安装应用"""
    print(f"{Fore.YELLOW}Online installation feature is under development{Style.RESET_ALL}")
    self.error_code = ErrorCodeManager().get_code(NotImplementedError)

def install_local(self, args):
    """安装本地应用到第三方命令目录（仅支持 Python 3.10+）
    参数格式: install-local <source_file_path> [command_name]
    """
    if len(args) < 2:
        print(f"Error: {Fore.RED}No source file specified.{Style.RESET_ALL}")
        print(f"Usage: install-local <source_file_path> [command_name]")
        return

    # 解析源文件路径（自动处理 ~ 和相对路径）
    source_path = os.path.abspath(os.path.expanduser(args[1]))
    
    # 获取命令名称（默认使用源文件名）
    cmd_name = args[2].replace('.py', '') if len(args) > 2 else \
               os.path.splitext(os.path.basename(source_path))[0]

    # 验证命令名有效性
    if not cmd_name.isidentifier():
        print(f"Error: {Fore.RED}Invalid command name '{cmd_name}'. Must be a valid Python identifier.{Style.RESET_ALL}")
        return

    # 检查命令是否已存在
    if any(cmd_name in cmds for cmds in CommandManager(self).allcmds.values()):
        print(f"Error: {Fore.RED}Command '{cmd_name}' already exists!{Style.RESET_ALL}")
        return

    # 检查并验证源文件
    if not os.path.isfile(source_path):
        print(f"Error: {Fore.RED}Source file not found: {source_path}{Style.RESET_ALL}")
        return

    try:
        # Python 3.10+ 标准方式验证模块
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location(cmd_name, source_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error: {Fore.RED}Invalid Python file: {type(e).__name__}: {e}{Style.RESET_ALL}")
        return

    # 准备目标目录
    target_dir = os.path.join("cmdList", "third_party")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, f"{cmd_name}.py")

    # 复制文件
    try:
        shutil.copy2(source_path, target_path)
        print(f"• {Fore.GREEN}Copied to: {target_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error: {Fore.RED}File copy failed: {type(e).__name__}: {e}{Style.RESET_ALL}")
        return

    # 更新配置
    if cmd_name not in cfg["commands"]["Third-party"]:
        cfg["commands"]["Third-party"].append(cmd_name)
    
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {Fore.RED}Config update failed: {type(e).__name__}: {e}{Style.RESET_ALL}")
        if os.path.exists(target_path):
            os.remove(target_path)
        return

    # 加载帮助信息
    success_msg = f"Command '{cmd_name}' installed successfully!"
    if hasattr(help, 'execute'):
        try:
            help.execute(self, [cmd_name])
            print(f"• {Fore.GREEN}{success_msg}{Style.RESET_ALL}")
        except:
            print(f"• {Fore.GREEN}{success_msg} (help load failed){Style.RESET_ALL}")
    else:
        print(f"• {Fore.GREEN}{success_msg}{Style.RESET_ALL}")
        
def remove_app(self, args):
    """移除已安装应用"""
    if len(args) < 2:
        print(f"Error: {Fore.RED}No app name specified for removal.{Style.RESET_ALL}")
        print(f"Usage: remove <app_name>")
        return
    
    app_name = args[1]
    if app_name not in cfg["commands"]["Third-party"]:
        print(f"Error: {Fore.RED}App '{app_name}' is not installed.{Style.RESET_ALL}")
        return
    
    try:
        # 从配置中移除
        cfg["commands"]["Third-party"].remove(app_name)
        
        # 删除命令文件
        third_party_dir = os.path.join("cmdList", "third_party")
        py_file = os.path.join(third_party_dir, f"{app_name}.py")
        
        if os.path.exists(py_file):
            os.remove(py_file)
            print(f"• {Fore.GREEN}App '{app_name}' removed successfully!{Style.RESET_ALL}")
        else:
            print(f"Warning: {Fore.YELLOW}Could not find '{py_file}', but removed from configuration.{Style.RESET_ALL}")
        
        # 保存配置
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
            
    except Exception as e:
        print(f"Error removing app: {Fore.RED}{e}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)

def list_apps(self, args):
    print(Back.BLUE + " Installed Apps ")
    print("\n".join(cfg["commands"]["Third-party"]))