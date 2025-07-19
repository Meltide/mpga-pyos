import importlib
import os
import subprocess
import shutil
from typing import Optional, Dict
from rich import print
from .basic import *

from .config import *
from .err import *

class CommandManager:
    def __init__(self, core, _cmd=""):
        self.cmd = _cmd
        self.core = core
        self.allcmds = SIGNED_COMMANDS  # 所有内置命令
        self.cmds = [
            cmd for category in self.allcmds.values() for cmd in category
        ]  # 所有命令列表
        self.package_info_cache: Dict[str, dict] = {}  # 包信息缓存

    def reg(self, cmd):
        """注册当前命令"""
        self.cmd = cmd

    def resolve_package_path(self) -> Optional[str]:
        """解析命令对应的包路径"""
        # 检查是否是包形式安装的命令
        pkg_dir = os.path.join("cmdList", "third_party", self.cmd)
        if os.path.isdir(pkg_dir):
            return pkg_dir

        # 检查是否是单文件形式
        pkg_file = os.path.join("cmdList", "third_party", f"{self.cmd}.py")
        if os.path.isfile(pkg_file):
            return pkg_file

        return None

    def pkg_name(self) -> str:
        pkg_path = self.resolve_package_path()
        
        if pkg_path and os.path.isdir(pkg_path):
            package_json_path = os.path.join(pkg_path, "package.json")
            if os.path.exists(package_json_path):
                with open(package_json_path, "r", encoding="utf-8") as f:
                    pkg_info = json.load(f)
                
                # 获取 main_file 并规范化路径
                main_file = pkg_info.get("main_file", "ciallo/ciallo.py")  # 默认值
                main_module = os.path.splitext(main_file)[0]  # 去掉 .py
                main_module = main_module.replace("/", ".")
                
                # 组合完整模块路径
                return f"cmdList.third_party.{main_module}"
        
        elif pkg_path:  # 单文件形式
            return f"cmdList.third_party.{os.path.splitext(self.cmd)[0]}"
        
        return f"cmdList.{self.cmd}"  # 内置命令

    def is_package(self) -> bool:
        """判断当前命令是否是包形式"""
        pkg_path = self.resolve_package_path()
        return pkg_path is not None and os.path.isdir(pkg_path)

    def get_package_info(self) -> Optional[dict]:
        """获取当前命令的package.json信息"""
        if self.cmd in self.package_info_cache:
            return self.package_info_cache[self.cmd]

        pkg_path = self.resolve_package_path()
        if not pkg_path or not os.path.isdir(pkg_path):
            return None

        package_json = os.path.join(pkg_path, "package.json")
        if os.path.exists(package_json):
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    info = json.load(f)
                    self.package_info_cache[self.cmd] = info
                    return info
            except (json.JSONDecodeError, IOError):
                pass
        return None

    def hasattr(self, attr) -> bool:
        """检查命令模块是否具有指定属性"""
        try:
            pkg = self.getpkg()
            return hasattr(pkg, attr)
        except ImportError:
            return False

    def loaded_cmd(self) -> bool:
        """检查命令是否已加载"""
        return self.cmd in self.cmds

    def getpkg(self):
        """导入命令对应的模块"""
        return importlib.import_module(self.pkg_name())

    def execute(self, username, args=()):
        """执行命令"""
        if args is None:
            args = ()  # 确保 args 是一个元组

        if not self.loaded_cmd():
            with open(os.path.join("configs", "Users", username, "user_policys.json"), "r", encoding="utf-8") as f:
                user_policys = json.load(f)
            if user_policys["system_commands"]:
                self._execute_system_command(args)
            else:
                raise ImportError(f"Command '{self.cmd}' not found")
            return

        try:
            module = self.getpkg()
            if hasattr(module, "execute"):
                # 传递 core 对象和参数给命令
                module.execute(self.core, args)
            else:
                raise AttributeError(f"Command '{self.cmd}' has no execute function")
        except Exception as e:
            self.core.error_code = ErrorCodeManager().get_code(e)
            raise  # 将异常传递给上层处理

    def _execute_system_command(self, args):
        """执行系统命令"""
        try:
            subprocess.run([self.cmd] + list(args), check=True)
        except subprocess.CalledProcessError as e:
            self.core.error_code = ErrorCodeManager().get_code(e)
            raise RuntimeError(f"System command failed: {e}")


class PathManager:
    def __init__(self, core):
        self.core = core
        self.basepath = BASEPATH

    def real_to_fake(self, path: str, userspace=False):
        """将真实路径转换为虚拟路径"""
        basepath = (
            os.path.join(self.basepath, "vm/home", self.core.account_names)
            if userspace
            else self.basepath
        )
        assert path.startswith(basepath.replace("\\", "/")), "Path not in userspace"
        return os.path.relpath(path, basepath).replace("\\", "/")

    def fake_to_real(self, path: str, userspace=False):
        """将虚拟路径转换为真实路径"""
        basepath = (
            os.path.join(self.basepath, "vm/home", self.core.account_names)
            if userspace
            else self.basepath
        )
        assert path.startswith(basepath.replace("\\", "/")), "Path not in userspace"
        return os.path.join(basepath, path.replace("\\", "/"))


class ErrorCodeManager:
    def __init__(self):
        self.info = EXCEPTION_INFO
        self.returns = EXCEPTION_RETURNS

    def get_code(self, e):
        """获取错误码"""
        if isinstance(e, (BaseException, Exception)):
            return self.returns.get(type(e), 0)
        elif isinstance(e, type):
            return self.returns.get(e, 0)
        else:
            return

    def get_type(self, code):
        """获取错误类型"""
        for k, v in self.returns.items():
            if v == code:
                return k.__name__
        return "UnknownException"

    def get_info(self, code_or_e):
        """获取错误信息"""
        if isinstance(code_or_e, int):
            return self.info.get(code_or_e, self.get_type(code_or_e))
        else:
            return self.info.get(self.get_code(code_or_e), type(code_or_e).name)


class HelpManager:
    def __init__(self, core, args=()):
        self.core = core
        self.cmdman = CommandManager(self.core)
        self.basic = Basic()
        self.args = self.basic.clean_args(
            args
        )  # 过滤和清理参数，只保留字符串类型的有效命令名
        self.cmd_name = self.args[0] if self.args else ""
        self.cmdman.reg(self.cmd_name)

    def get_package_doc(self, cmd_name):
        """获取包中package.json中的描述信息"""
        package_json = os.path.join("cmdList", "third_party", cmd_name, "package.json")
        if os.path.exists(package_json):
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    package_info = json.load(f)
                    return package_info.get("description", "No description available")
            except (json.JSONDecodeError, IOError):
                return "Invalid package.json"
        return None
    
    def get_package_usage(self, cmd_name):
        """获取包中package.json中的描述信息"""
        package_json = os.path.join("cmdList", "third_party", cmd_name, "package.json")
        if os.path.exists(package_json):
            try:
                with open(package_json, "r", encoding="utf-8") as f:
                    package_info = json.load(f)
                    return package_info.get("usage", "No usage available")
            except (json.JSONDecodeError, IOError):
                return "Invalid package.json"
        return None

    def show_all(self):
        """显示所有命令"""
        print("Available Commands:")
        print("* Third-party apps will be highlighted")
        for category, cmds in self.cmdman.allcmds.items():
            print(f"[blue] {category} [/]")
            for cmd in sorted(cmds):
                self.cmdman.reg(cmd)
                try:
                    if self.cmdman.is_package():
                        # 如果是包，从 package.json 获取描述
                        doc = self.get_package_doc(cmd) or "No description"
                        print(f"[yellow]{cmd:<15}[/] {doc}")
                    else:
                        # 内置命令
                        doc = self.cmdman.getpkg().__doc__ or "No description"
                        print(f"{cmd:<15}[/] {doc}")
                except ImportError:
                    print(f"{cmd:<15}[/] (Not loadable)")
        return

    def show_cmd(self):
        """显示指定命令的帮助信息"""
        # 检查命令是否存在
        if not self.cmdman.loaded_cmd():
            raise FileNotFoundError(
                f"Command '{self.cmd_name}' not found.Type 'help' to see available commands"
            )

    def show_info(self):
        """显示指定命令的详细信息"""
        try:
            pkg = self.cmdman.getpkg()
            print(f"[white on green] Help for: {self.cmd_name} [/]")
    
            # 显示描述
            if self.cmdman.is_package():
                description = self.get_package_doc(self.cmd_name) or "No description"
            else:
                description = getattr(pkg, "__doc__", "No description available")
            print(f"[blue] Description: {self.cmd_name} [/]")
            print('  '+description.strip())
    
            # 显示用法
            if self.cmdman.is_package():
                usage = self.get_package_usage(self.cmd_name) or "No usage available"
            else:
                usage = getattr(pkg, "__usage__", "No usage available")
    
            print(f"[blue] Usage: [/]")
            if isinstance(usage, dict):  # 如果是字典，按键值对显示
                for example, desc in usage.items():
                    print(f"  {self.cmd_name} [green]{example:<15}[/] {desc}")
            elif isinstance(usage, str):  # 如果是字符串，直接显示
                print(f"  {usage}")
            else:
                print(f"[yellow]No usage examples available[/]")
    
        except Exception as e:
            raise RunningError(f"Error loading command help: {str(e)}")