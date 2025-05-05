import json, shutil, os, importlib
import zipfile
import subprocess
import sys
from utils.config import cfg
from . import help, sysname
from utils.man import ErrorCodeManager
from utils.man import CommandManager
from colorama import Fore, Back, Style

__doc__ = "YET Package manager"  # 第三方命令注册模块

__usage__ = {
    "install": "Install a local app (supports .py files or .zip/.mpk packages)",
    "remove": "Remove apps",
    "list": "List all third-party apps",
    "deps": "Manage dependencies for an app",
    "info": "Show package information"
}

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
        case "remove":
            remove_app(self, args)
        case "list":
            list_apps(self, args)
        case "deps":
            manage_dependencies(self, args)
        case "info":
            show_package_info(self, args)
        case _:
            print(f"Error: {Fore.RED}Unknown command '{args[0]}'.")
            print("Usage:")
            for command, description in __usage__.items():
                print(f"  {command}: {description}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)

def install(self, args):
    """安装本地应用或ZIP包到第三方命令目录
    参数格式: install <source_path> [command_name]
    """
    if len(args) < 2:
        print(f"Error: {Fore.RED}No source file specified.{Style.RESET_ALL}")
        print(f"Usage: install <source_path> [command_name]")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    source_path = os.path.abspath(os.path.expanduser(args[1]))
    
    # 如果是ZIP或MPK文件，先解压
    if source_path.endswith(('.zip', '.mpk')):
        install_from_package(self, source_path, args[2] if len(args) > 2 else None)
        return
    
    # 原始的单文件安装逻辑
    cmd_name = args[2].replace('.py', '') if len(args) > 2 else \
               os.path.splitext(os.path.basename(source_path))[0]

    if not cmd_name.isidentifier():
        print(f"Error: {Fore.RED}Invalid command name '{cmd_name}'. Must be a valid Python identifier.{Style.RESET_ALL}")
        return

    if any(cmd_name in cmds for cmds in CommandManager(self).allcmds.values()):
        print(f"Error: {Fore.RED}Command '{cmd_name}' already exists!{Style.RESET_ALL}")
        return

    if not os.path.isfile(source_path):
        print(f"Error: {Fore.RED}Source file not found: {source_path}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(FileNotFoundError)
        return

    try:
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location(cmd_name, source_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error: {Fore.RED}Invalid Python file: {type(e).__name__}: {e}{Style.RESET_ALL}")
        return

    target_dir = os.path.join("cmdList", "third_party")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, f"{cmd_name}.py")

    try:
        shutil.copy2(source_path, target_path)
        print(f"• {Fore.GREEN}Copied to: {target_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error: {Fore.RED}File copy failed: {type(e).__name__}: {e}{Style.RESET_ALL}")
        return

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

    # 检查并安装依赖
    install_dependencies(self, cmd_name, target_path)

    success_msg = f"Command '{cmd_name}' installed successfully!"
    if hasattr(help, 'execute'):
        try:
            help.execute(self, [cmd_name])
            print(f"• {Fore.GREEN}{success_msg}{Style.RESET_ALL}")
        except:
            print(f"• {Fore.GREEN}{success_msg} (help load failed){Style.RESET_ALL}")
    else:
        print(f"• {Fore.GREEN}{success_msg}{Style.RESET_ALL}")

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
        package_info = read_package_info(temp_dir)
        
        # 如果没有指定命令名，尝试从package.json获取或使用主模块名
        if not cmd_name:
            if package_info and 'package' in package_info:
                cmd_name = package_info['package']
            else:
                main_module = find_main_module(temp_dir)
                if not main_module:
                    print(f"Error: {Fore.RED}Could not find main module in the package.{Style.RESET_ALL}")
                    self.error_code = ErrorCodeManager().get_code(SyntaxError)
                    shutil.rmtree(temp_dir)
                    return
                cmd_name = os.path.splitext(os.path.basename(main_module))[0]
        
        # 验证命令名
        if not cmd_name.isidentifier():
            print(f"Error: {Fore.RED}Invalid command name '{cmd_name}'. Must be a valid Python identifier.{Style.RESET_ALL}")
            self.error_code = ErrorCodeManager().get_code(NameError)
            shutil.rmtree(temp_dir)
            return
            
        # 检查命令是否已存在
        if any(cmd_name in cmds for cmds in CommandManager(self).allcmds.values()):
            print(f"Error: {Fore.RED}Command '{cmd_name}' already exists!{Style.RESET_ALL}")
            self.error_code = ErrorCodeManager().get_code(SyntaxError)
            shutil.rmtree(temp_dir)
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
        if cmd_name not in cfg["commands"]["Third-party"]:
            cfg["commands"]["Third-party"].append(cmd_name)
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)
        
        # 检查并安装依赖
        main_module_path = os.path.join(target_dir, find_main_module(target_dir) or 'main.py')
        install_dependencies(self, cmd_name, main_module_path, package_info)
        
        print(f"• {Fore.GREEN}Package '{cmd_name}' installed successfully!{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"Error: {Fore.RED}Failed to install from package: {type(e).__name__}: {e}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)
    finally:
        # 清理临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def read_package_info(directory):
    """读取package.json文件"""
    package_json = os.path.join(directory, "package.json")
    if os.path.exists(package_json):
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: {Fore.YELLOW}Invalid package.json: {e}{Style.RESET_ALL}")
    return None

def find_main_module(directory):
    """在目录中查找主模块"""
    # 1. 检查是否有main.py
    if os.path.exists(os.path.join(directory, "main.py")):
        return "main.py"
    
    # 2. 检查是否有与目录同名的.py文件
    dir_name = os.path.basename(directory)
    possible_main = f"{dir_name}.py"
    if os.path.exists(os.path.join(directory, possible_main)):
        return possible_main
    
    # 3. 查找其他.py文件
    py_files = [f for f in os.listdir(directory) if f.endswith('.py')]
    if len(py_files) == 1:
        return py_files[0]
    
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
    print(f"Package: {Fore.CYAN}{package_info.get('package', pkg_name)}{Style.RESET_ALL}")
    print(f"Version: {Fore.GREEN}{package_info.get('version', 'unknown')}{Style.RESET_ALL}")
    
    if 'description' in package_info:
        print(f"Description: {package_info['description']}")
    
    if 'author' in package_info:
        print(f"Author: {Fore.BLUE}{package_info['author']}{Style.RESET_ALL}")
    
    if 'dependences' in package_info:
        print(f"Dependencies: {Fore.YELLOW}{', '.join(package_info['dependences'])}{Style.RESET_ALL}")

def manage_dependencies(self, args):
    """管理应用依赖"""
    if len(args) < 2:
        print(f"Error: {Fore.RED}No command specified.{Style.RESET_ALL}")
        print(f"Usage: deps <command_name> [install|list]")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return
    
    cmd_name = args[1]
    action = args[2] if len(args) > 2 else "list"
    
    # 查找命令文件
    cmd_path = None
    for root, _, files in os.walk(os.path.join("cmdList", "third_party")):
        for file in files:
            if file.startswith(cmd_name) and file.endswith('.py'):
                cmd_path = os.path.join(root, file)
                break
        if cmd_path:
            break
    
    if not cmd_path:
        print(f"Error: {Fore.RED}Command '{cmd_name}' not found.{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(FileNotFoundError)
        return
    
    if action == "install":
        install_dependencies(self, cmd_name, cmd_path)
    elif action == "list":
        list_dependencies(self, cmd_name, cmd_path)
    else:
        print(f"Error: {Fore.RED}Unknown action '{action}'. Use 'install' or 'list'.{Style.RESET_ALL}")

def list_dependencies(self, cmd_name, module_path):
    """列出应用依赖"""
    try:
        # 检查requirements.txt
        req_file = os.path.join(os.path.dirname(module_path), "requirements.txt")
        if os.path.exists(req_file):
            print(f"• {Fore.YELLOW}Dependencies from requirements.txt:{Style.RESET_ALL}")
            with open(req_file, 'r') as f:
                print(f.read())
            return
        
        # 检查模块中的__dependencies__
        spec = importlib.util.spec_from_file_location(cmd_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, '__dependencies__'):
            deps = getattr(module, '__dependencies__')
            if isinstance(deps, (list, tuple)) and deps:
                print(f"• {Fore.YELLOW}Module dependencies:{Style.RESET_ALL}")
                for dep in deps:
                    print(f"  - {dep}")
                return
        
        print(f"• {Fore.YELLOW}No dependencies found for '{cmd_name}'.{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"Error: {Fore.RED}Could not list dependencies: {type(e).__name__}: {e}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)

def remove_app(self, args):
    """移除已安装应用"""
    if len(args) < 2:
        print(f"Error: {Fore.RED}No app name specified for removal.{Style.RESET_ALL}")
        print(f"Usage: remove <app_name>")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return
    
    app_name = args[1]
    if app_name not in cfg["commands"]["Third-party"]:
        print(f"Error: {Fore.RED}App '{app_name}' is not installed.{Style.RESET_ALL}")
        return
    
    try:
        # 从配置中移除
        cfg["commands"]["Third-party"].remove(app_name)
        
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
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
            
    except Exception as e:
        print(f"Error removing app: {Fore.RED}{e}{Style.RESET_ALL}")
        self.error_code = ErrorCodeManager().get_code(e)

def list_apps(self, args):
    print(Back.BLUE + " Installed Apps " + Style.RESET_ALL)
    for app in cfg["commands"]["Third-party"]:
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