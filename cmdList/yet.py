import json, shutil, os, importlib
import zipfile
import subprocess
import sys
from utils.config import commands
from . import help, sysname
from utils.man import ErrorCodeManager
from utils.man import CommandManager
from colorama import Fore, Back, Style

__doc__ = "YET Package manager"  # 第三方命令注册模块

__usage__ = {
    "install": "Install a local app",
    "remove": "Remove apps",
    "list": "List all third-party apps",
    "info": "Show package information"
}

# 全局命令缓存字典
_command_cache = {}

def execute(self, args):
    """主执行函数"""
    if not args:
        print(f"Error: {Fore.RED}No arguments provided. Please specify a valid command.")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return
    
    match args[0]:
        case "install":
            install(self, args)
            _auto_reload_commands(self)  # 安装后自动重载
        case "remove":
            remove_app(self, args)
            _auto_reload_commands(self)  # 移除后自动重载
        case "list":
            list_apps(self, args)
        case "info":
            show_package_info(self, args)
        case _:
            print(f"Error: {Fore.RED}Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)

def _auto_reload_commands(self):
    """自动重载所有第三方命令"""
    global _command_cache
    
    # 1. 清除已加载的命令模块
    for cmd in list(sys.modules.keys()):
        if cmd.startswith('cmdList.third_party.'):
            del sys.modules[cmd]
    
    # 2. 重新扫描命令目录
    third_party_dir = os.path.join("cmdList", "third_party")
    if not os.path.exists(third_party_dir):
        return
    
    # 3. 更新命令缓存
    _command_cache.clear()
    for item in os.listdir(third_party_dir):
        if item.endswith('.py') and not item.startswith('_'):
            cmd_name = item[:-3]
            try:
                module = importlib.import_module(f'cmdList.third_party.{cmd_name}')
                _command_cache[cmd_name] = module
                if cmd_name not in commands["commands"]["Third-party"]:
                    commands["commands"]["Third-party"].append(cmd_name)
            except Exception as e:
                print(f"{Fore.YELLOW}Warning: Failed to reload command '{cmd_name}': {e}{Style.RESET_ALL}")
    
    # 4. 保存配置
    try:
        with open(os.path.join("configs", "commands.json"), "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Failed to update config: {e}{Style.RESET_ALL}")

def get_command_module(self, cmd_name):
    """获取缓存的命令模块"""
    global _command_cache
    
    # 如果命令在缓存中且模块存在，直接返回
    if cmd_name in _command_cache:
        module = _command_cache[cmd_name]
        if module and module.__file__ and os.path.exists(module.__file__):
            return module
    
    # 否则尝试动态加载
    try:
        module = importlib.import_module(f'cmdList.third_party.{cmd_name}')
        _command_cache[cmd_name] = module  # 更新缓存
        return module
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Failed to load command '{cmd_name}': {e}{Style.RESET_ALL}")
        return None

def install(self, args):
    """安装应用并自动重载"""
    global source_path

    if len(args) < 2:
        print(f"Error: {Fore.RED}No source file specified.{Style.RESET_ALL}")
        print(f"Usage: install <source_path> [command_name]")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    source_path = os.path.abspath(os.path.expanduser(args[1]))

    # ZIP/MPK包处理
    if source_path.endswith(('.zip', '.mpk')):
        install_from_package(self, source_path, args[2] if len(args) > 2 else None)
        _auto_reload_commands(self)  # 动态重载命令
        return

    # 单文件安装
    cmd_name = args[2].replace('.py', '') if len(args) > 2 else \
               os.path.splitext(os.path.basename(source_path))[0]

    # 检查命令是否已存在（包括原生命令）
    all_commands = []
    for cmd_type in CommandManager(self).allcmds.values():
        all_commands.extend(cmd_type)
    if cmd_name in all_commands:
        print(f"Error: {Fore.RED}Command '{cmd_name}' already exists!{Style.RESET_ALL}")
        return

    # 验证Python文件有效性
    try:
        spec = importlib.util.spec_from_file_location(cmd_name, source_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error: {Fore.RED}Invalid Python file: {type(e).__name__}: {e}{Style.RESET_ALL}")
        return

    # 复制文件到目标目录
    target_dir = os.path.join("cmdList", "third_party")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, f"{cmd_name}.py")

    try:
        shutil.copy2(source_path, target_path)
        print(f"• {Fore.GREEN}Copied to: {target_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error: {Fore.RED}File copy failed: {type(e).__name__}: {e}{Style.RESET_ALL}")
        return

    # 安装依赖
    install_dependencies(self, cmd_name, target_path)

    # 动态加载新命令
    try:
        module = importlib.import_module(f'cmdList.third_party.{cmd_name}')
        _command_cache[cmd_name] = module
        if cmd_name not in commands["commands"]["Third-party"]:
            commands["commands"]["Third-party"].append(cmd_name)
        print(f"• {Fore.GREEN}Command '{cmd_name}' installed and loaded successfully!{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error: {Fore.RED}Failed to load command '{cmd_name}': {e}{Style.RESET_ALL}")
        return

    # 保存配置
    try:
        with open(os.path.join("configs", "commands.json"), "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: {Fore.YELLOW}Failed to update config: {e}{Style.RESET_ALL}")

def install_from_package(self, package_path, cmd_name=None):
    """从ZIP/MPK包安装应用"""
    try:
        # 创建临时解压目录
        temp_dir = os.path.join("cmdList", "temp_install")
        os.makedirs(temp_dir, exist_ok=True)
        
        # 解压包文件
        with zipfile.ZipFile(package_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            print(f"• {Fore.GREEN}Extracted package to: {temp_dir}{Style.RESET_ALL}")
        
        # 检查是否有package.json
        package_info = read_package_info(temp_dir)  # 调用函数，确保 version_code 存在
        
        # 如果没有指定命令名，尝试从package.json获取或使用主模块名
        if not cmd_name:
            if package_info and 'command' in package_info:
                cmd_name = package_info['command']
            else:
                raise NameError("Missing package name")
        
        # 获取已安装版本的 version_code
        old_version_code = get_installed_version_code(self, cmd_name)
        new_version_code = int(package_info.get("version_code", 0))  # 新包的 version_code
        
        # 检查是否已存在
        if old_version_code is not None and new_version_code < old_version_code:
            print(f"Error: {Fore.RED}Cannot install an older version (installed: {old_version_code}, new: {new_version_code}).{Style.RESET_ALL}")
            return
        
        # 创建目标目录
        target_dir = os.path.join("cmdList", "third_party", cmd_name)
        os.makedirs(target_dir, exist_ok=True)
        
        # 移动所有文件到目标目录
        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = os.path.join(target_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        
        # 更新配置
        category = package_info.get("category", "Other")
        if category in commands["commands"]:
            commands["commands"][category].append(cmd_name)
        else:
            commands["commands"][category] = [cmd_name]
        
        with open(os.path.join("configs", "commands.json"), "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4, ensure_ascii=False)
        
        # 检查并安装依赖
        main_module_path = os.path.join(target_dir, find_main_module(target_dir) or 'main.py')
        install_dependencies(self, cmd_name, main_module_path, package_info)
        
        print(f"• {Fore.GREEN}Package '{cmd_name}' installed successfully!{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"Error: {Fore.RED}Failed to install: {type(e).__name__ if not str(e) else e}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)
    finally:
        # 清理临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def get_installed_version_code(self, cmd_name):
    """获取已安装软件的 version_code"""
    # 检测包目录
    pkg_dir = os.path.join("cmdList", "third_party", cmd_name)
    pkg_info = os.path.join(pkg_dir, "package.json")
    if os.path.exists(pkg_info):
        with open(pkg_info, 'r', encoding='utf-8') as f:
            info = json.load(f)
            return int(info.get('version_code', 0))  # 返回 version_code，默认为 0
    
    return None

def read_package_info(directory):
    """读取package.json文件并检查version_code"""
    package_json = os.path.join(directory, "package.json")
    if os.path.exists(package_json):
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                package_info = json.load(f)
                # 检查是否包含 version_code
                if "version_code" not in package_info:
                    raise KeyError("Missing 'version_code' in package.json")
                    return
                return package_info
        except Exception as e:
            raise
    else:
        raise FileNotFoundError("Missing package.json")
    return None

def find_main_module(directory):
    """在目录中查找主模块"""
    # 检查是否有main.py
    if os.path.exists(os.path.join(directory, "main.py")):
        return "main.py"

    return None

def install_dependencies(self, cmd_name, module_path, package_info=None):
    """自动安装依赖"""
    try:
        # 优先使用package.json中的依赖
        if package_info and 'dependences' in package_info:
            deps = package_info['dependences']
            if isinstance(deps, (list, tuple)) and deps:
                print(f"• {Fore.YELLOW}Found dependencies in package.json, installing...{Style.RESET_ALL}")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install"] + list(deps))
                    print(f"• {Fore.GREEN}Dependencies installed successfully!{Style.RESET_ALL}")
                    return  # 如果package.json有依赖，就不再检查其他来源
                except subprocess.CalledProcessError as e:
                    print(f"Warning: {Fore.YELLOW}Failed to install some dependencies: {e}{Style.RESET_ALL}")
                    self.error_code = ErrorCodeManager().get_code(e)
        
        # 检查是否有requirements.txt在同一目录
        req_file = os.path.join(os.path.dirname(module_path), "requirements.txt")
        if os.path.exists(req_file):
            print(f"• {Fore.YELLOW}Found requirements.txt, installing dependencies...{Style.RESET_ALL}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
                print(f"• {Fore.GREEN}Dependencies installed successfully!{Style.RESET_ALL}")
            except subprocess.CalledProcessError as e:
                print(f"Warning: {Fore.YELLOW}Failed to install some dependencies: {e}{Style.RESET_ALL}")
                self.error_code = ErrorCodeManager().get_code(e)
        
        # 检查模块中是否有__dependencies__变量
        elif os.path.exists(module_path):
            try:
                spec = importlib.util.spec_from_file_location(cmd_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, '__dependencies__'):
                    deps = getattr(module, '__dependencies__')
                    if isinstance(deps, (list, tuple)) and deps:
                        print(f"• {Fore.YELLOW}Found dependencies in module, installing...{Style.RESET_ALL}")
                        try:
                            subprocess.check_call([sys.executable, "-m", "pip", "install"] + list(deps))
                            print(f"• {Fore.GREEN}Dependencies installed successfully!{Style.RESET_ALL}")
                        except subprocess.CalledProcessError as e:
                            print(f"Warning: {Fore.YELLOW}Failed to install some dependencies: {e}{Style.RESET_ALL}")
                            self.error_code = ErrorCodeManager().get_code(e)
            except:
                pass
                    
    except Exception as e:
        print(f"Warning: {Fore.YELLOW}Could not check dependencies: {type(e).__name__}: {e}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)

def show_package_info(self, args):
    """显示包信息"""
    if len(args) < 2:
        print(f"Error: {Fore.RED}No package specified.{Style.RESET_ALL}")
        print(f"Usage: info <package_name>")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return
    
    pkg_name = args[1]
    
    # 查找包目录
    pkg_dir = os.path.join("cmdList", "third_party", pkg_name)
    if not os.path.exists(pkg_dir):
        # 可能是单文件应用
        pkg_file = os.path.join("cmdList", "third_party", f"{pkg_name}.py")
        if not os.path.exists(pkg_file):
            print(f"Error: {Fore.RED}Package '{pkg_name}' not found.{Style.RESET_ALL}")
            self.error_code = ErrorCodeManager().get_code(FileNotFoundError)
            return
        
        print(f"Package: {Fore.CYAN}{pkg_name}{Style.RESET_ALL}")
        print(f"Type: {Fore.YELLOW}Single file{Style.RESET_ALL}")
        return
    
    # 读取package.json
    package_info = read_package_info(pkg_dir)
    if not package_info:
        print(f"Package: {Fore.CYAN}{pkg_name}{Style.RESET_ALL}")
        print(f"Type: {Fore.YELLOW}Directory (no package.json){Style.RESET_ALL}")
        return
    
    # 显示包信息
    print(f"Package: {Fore.CYAN}{package_info.get('command', pkg_name)}{Style.RESET_ALL}")
    print(f"Version: {Fore.GREEN}{package_info.get('version', 'unknown')}{Style.RESET_ALL}")
    print(f"Version Code: {Fore.GREEN}{package_info.get('version_code', 'unknown')}{Style.RESET_ALL}")
    print(f"Category: {Fore.BLUE}{package_info.get('category', 'Other')}{Style.RESET_ALL}")
    
    if 'description' in package_info:
        print(f"Description: {package_info['description']}")
    
    if 'author' in package_info:
        print(f"Author: {Fore.BLUE}{package_info['author']}{Style.RESET_ALL}")
    
    if 'dependences' in package_info:
        print("Dependencies:")
        for dependence in sorted(package_info['dependences']):
            print(f"- {Fore.YELLOW}{dependence}{Fore.RESET}")

def remove_app(self, args):
    """移除已安装应用"""
    if len(args) < 2:
        print(f"Error: {Fore.RED}No app name specified for removal.{Style.RESET_ALL}")
        print(f"Usage: remove <app_name>")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return
    
    app_name = args[1]
    
    # 查找包目录
    pkg_dir = os.path.join("cmdList", "third_party", app_name)
    if not os.path.exists(pkg_dir):
        pkg_file = os.path.join("cmdList", "third_party", f"{pkg_name}.py")
        if not os.path.exists(pkg_file):
            raise FileNotFoundError(f"Package '{pkg_name}' not found.")
            return
        return
    
    # 读取package.json
    package_info = read_package_info(pkg_dir)
    if not package_info:
        print(f"Package: {Fore.CYAN}{pkg_name}{Style.RESET_ALL}")
        print(f"Type: {Fore.YELLOW}Directory (no package.json){Style.RESET_ALL}")
        return
    
    category = package_info.get('category', 'Other')
    
    if app_name not in commands["commands"][category]:
        print(f"Error: {Fore.RED}App '{app_name}' is not installed.{Style.RESET_ALL}")
        return
    
    try:
        # 从配置中移除
        commands["commands"][category].remove(app_name)
        if len(commands["commands"][category]) <= 1:
            del commands["commands"][category]
        
        # 删除命令文件或目录
        third_party_dir = os.path.join("cmdList", "third_party")
        py_file = os.path.join(third_party_dir, f"{app_name}.py")
        app_dir = os.path.join(third_party_dir, app_name)
        
        if os.path.exists(py_file):
            os.remove(py_file)
            print(f"• {Fore.GREEN}App '{app_name}' removed successfully!{Style.RESET_ALL}")
        elif os.path.exists(app_dir):
            shutil.rmtree(app_dir)
            print(f"• {Fore.GREEN}App '{app_name}' removed successfully!{Style.RESET_ALL}")
        else:
            print(f"Warning: {Fore.YELLOW}Could not find app files, but removed from configuration.{Style.RESET_ALL}")
        
        # 保存配置
        with open(os.path.join("configs", "commands.json"), "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4)
            
    except Exception as e:
        print(f"Error removing app: {Fore.RED}{e}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)

def list_apps(self, args):
    print(Back.BLUE + " Installed Apps " + Style.RESET_ALL)
    for app in commands["commands"]["Third-party"]:
        # 检查是单文件还是目录
        app_path = os.path.join("cmdList", "third_party", f"{app}.py")
        if os.path.exists(app_path):
            print(f"• {app} (single file)")
        else:
            app_dir = os.path.join("cmdList", "third_party", app)
            if os.path.exists(app_dir):
                print(f"• {app} (package)")
            else:
                print(f"• {app} (missing files)")