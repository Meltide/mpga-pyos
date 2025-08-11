import json, shutil, os, importlib
import zipfile
import subprocess
import sys
import pwinput
import base64

from .config import *
from .man import ErrorCodeManager, CommandManager
from .err import RunningError
from rich import print

# 全局命令缓存字典
_command_cache = {}


def auth_passwd(self):
    stpasswd = base64.b64decode(profiles["accounts"][self.username]["passwd"].strip()).decode(
        "utf-8"
    )
    passwd = pwinput.pwinput("Password: ")
    if passwd != stpasswd:
        raise ValueError("Password incorrect.")


def auto_reload_commands(self):
    """自动重载所有第三方命令"""
    global _command_cache, SIGNED_COMMANDS

    # 1. 清除已加载的命令模块
    for cmd in list(sys.modules.keys()):
        if cmd.startswith("cmdList.third_party."):
            del sys.modules[cmd]

    # 2. 重新扫描命令目录
    third_party_dir = os.path.join("cmdList", "third_party")
    if not os.path.exists(third_party_dir):
        return

    # 3. 更新命令缓存并根据 package.json 分类
    _command_cache.clear()
    for item in os.listdir(third_party_dir):
        if item.endswith(".py") and not item.startswith("_"):
            cmd_name = item[:-3]
            try:
                module = importlib.import_module(f"cmdList.third_party.{cmd_name}")
                importlib.reload(module)  # 动态重新加载模块
                _command_cache[cmd_name] = module

                # 读取 package.json 获取分类
                package_json = os.path.join(third_party_dir, cmd_name, "package.json")
                category = "Other"  # 默认分类
                if os.path.exists(package_json):
                    try:
                        with open(package_json, "r", encoding="utf-8") as f:
                            package_info = json.load(f)
                            category = package_info.get("category", "Other")
                    except (json.JSONDecodeError, IOError):
                        print(f"[yellow]Warning: Invalid package.json for '{cmd_name}'[/]")

                # 确保分类存在于 commands
                if category not in commands["commands"]:
                    commands["commands"][category] = []

                # 添加命令到分类
                if cmd_name not in commands["commands"][category]:
                    commands["commands"][category].append(cmd_name)

            except Exception as e:
                print(
                    f"[yellow]Warning: Failed to reload command '{cmd_name}': {e}[/]"
                )

    # 更新 SIGNED_COMMANDS 和 CommandManager
    SIGNED_COMMANDS.update(commands["commands"])
    self.command_manager.allcmds = SIGNED_COMMANDS
    self.command_manager.cmds = [
        cmd for category in self.command_manager.allcmds.values() for cmd in category
    ]

    # 4. 保存配置
    try:
        with open(os.path.join("configs", "commands.json"), "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[yellow]Warning: Failed to update config: {e}[/]")


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
        module = importlib.import_module(f"cmdList.third_party.{cmd_name}")
        _command_cache[cmd_name] = module  # 更新缓存
        return module
    except Exception as e:
        print(f"[yellow]Warning: Failed to load command '{cmd_name}': {e}[/]")
        return None


def install(self, args):
    """安装应用并自动重载"""
    global source_path
    
    if self.NEED_PASSWD:
        auth_passwd(self)

    if len(args) < 2:
        print(f"Error: [red]No source file specified.[/]")
        print(f"Usage: install <source_path> [command_name]")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    source_path = os.path.abspath(os.path.expanduser(args[1]))

    # ZIP/MPK包处理
    if source_path.endswith((".zip", ".mpk")):
        install_from_package(self, source_path, args[2] if len(args) > 2 else None)
        auto_reload_commands(self)  # 动态重载命令
        return

    # 单文件安装
    cmd_name = (
        args[2].replace(".py", "")
        if len(args) > 2
        else os.path.splitext(os.path.basename(source_path))[0]
    )

    # 检查命令是否已存在（包括原生命令）
    all_commands = []
    for cmd_type in CommandManager(self).allcmds.values():
        all_commands.extend(cmd_type)
    if cmd_name in all_commands:
        print(f"Error: [red]Command '{cmd_name}' already exists![/]")
        return

    # 验证Python文件有效性
    try:
        spec = importlib.util.spec_from_file_location(cmd_name, source_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(
            f"Error: [red]Invalid Python file: {type(e).__name__}: {e}[/]"
        )
        return

    # 复制文件到目标目录
    target_dir = os.path.join("cmdList", "third_party")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, f"{cmd_name}.py")

    try:
        shutil.copy2(source_path, target_path)
        print(f"• [green]Copied to: {target_path}[/]")
    except Exception as e:
        print(
            f"Error: [red]File copy failed: {type(e).__name__}: {e}[/]"
        )
        return

    # 动态加载新命令
    try:
        module = importlib.import_module(f"cmdList.third_party.{cmd_name}")
        _command_cache[cmd_name] = module
        if cmd_name not in commands["commands"]["Third-party"]:
            commands["commands"]["Third-party"].append(cmd_name)
        print(
            f"• [green]Command '{cmd_name}' installed and loaded successfully![/]"
        )
    except Exception as e:
        print(
            f"Error: [red]Failed to load command '{cmd_name}': {e}[/]"
        )
        return

    # 保存配置
    try:
        with open(os.path.join("configs", "commands.json"), "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: [yellow]Failed to update config: {e}[/]")


def install_from_package(self, package_path, cmd_name=None):
    """从ZIP/MPK包安装应用"""
    try:
        # 创建临时解压目录
        temp_dir = os.path.join("cmdList", "temp_install")
        os.makedirs(temp_dir, exist_ok=True)

        # 解压包文件
        with zipfile.ZipFile(package_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            print(f"• [green]Extracted package to: {temp_dir}[/]")

        # 检查是否有package.json
        package_info = read_package_info(temp_dir)  # 调用函数，确保 version_code 存在

        # 如果没有指定命令名，尝试从package.json获取或使用主模块名
        if not cmd_name:
            if package_info and "command" in package_info:
                cmd_name = package_info["command"]
            else:
                raise NameError("Missing package name")

        # 获取已安装版本的 version_code
        old_version_code = get_installed_version_code(self, cmd_name)
        new_version_code = int(
            package_info.get("version_code", 0)
        )  # 新包的 version_code

        # 检查是否已存在
        all_commands = []
        app_installed = False

        for cmd_type in CommandManager(self).allcmds.values():
            all_commands.extend(cmd_type)
        if cmd_name in all_commands:
            app_installed = True

        if old_version_code is not None:
            match self.ASK_DOWNGRADE:
                case "ask":
                    if new_version_code < old_version_code:
                        print(
                            f"Warning: [yellow]You are executing a downgrade operation (installed: {old_version_code}, new: {new_version_code})[/]"
                        )
                        choice = input("Do you want to continue? [y/n]: ")
                        match choice:
                            case "n" | "N":
                                print("[yellow]Installition canceled.[/]")
                                return
                            case "Y" | "y" | "":
                                pass
                            case _:
                                raise NameError("Unknown command.")
                    elif new_version_code == old_version_code:
                        print(
                            f"[yellow]Same version detected ({new_version_code}), reinstalling...[/]"
                        )
                case "deny":
                    raise RunningError(f"Downgrade is not allowed (installed: {old_version_code}, new: {new_version_code})")
                case "allow":
                    print(f"Warning: [yellow]Downgrade is executing (installed: {old_version_code}, new: {new_version_code})[/]")
                case _:
                    raise SyntaxError(f"Unknown setting: '{self.ASK_DOWNGRADE}'")

        # 创建目标目录
        target_dir = os.path.join("cmdList", "third_party", cmd_name)
        os.makedirs(target_dir, exist_ok=True)

        # 检查并安装依赖
        main_module_path = os.path.join(
            target_dir, find_main_module(target_dir, package_info) or "main.py"
        )
        try:
            install_dependencies(self, cmd_name, main_module_path, package_info)
        except Exception as e:
            print(f"Error: [red]{e}[/]")
            shutil.rmtree(target_dir)
            self.error_code = ErrorCodeManager().get_code(e)
            return

        # 移动所有文件到目标目录
        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = os.path.join(target_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        # 更新配置
        if not app_installed:
            category = package_info.get("category", "Other")
            if category in commands["commands"]:
                commands["commands"][category].append(cmd_name)
            else:
                commands["commands"][category] = [cmd_name]

            with open(
                os.path.join("configs", "commands.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(commands, f, indent=4, ensure_ascii=False)

        print(
            f"• [green]Package '{cmd_name}' installed successfully![/]"
        )

    except Exception as e:
        raise RunningError(
            f"Failed to install: {type(e).__name__ if not str(e) else e}"
        )
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
        with open(pkg_info, "r", encoding="utf-8") as f:
            info = json.load(f)
            return int(info.get("version_code", 0))  # 返回 version_code，默认为 0

    return None


def read_package_info(directory):
    """读取package.json文件并检查version_code"""
    package_json = os.path.join(directory, "package.json")
    if os.path.exists(package_json):
        try:
            with open(package_json, "r", encoding="utf-8") as f:
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


def find_main_module(directory, package_info):
    """在目录中查找主模块"""
    if "main_file" in package_info:
        return package_info["main_file"]
    elif os.path.exists(os.path.join(directory, "main.py")):
        return "main.py"

    return None


def install_dependencies(self, cmd_name, module_path, package_info=None):
    """自动安装依赖"""
    # 优先使用package.json中的依赖
    if package_info and "dependencies" in package_info:
        deps = package_info["dependencies"]
        if isinstance(deps, (list, tuple)) and deps:
            print(
                f"• [yellow]Found dependencies in package.json, installing...[/]"
            )
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install"] + list(deps)
                )
                print(
                    f"• [green]Dependencies installed successfully![/]"
                )
                return  # 如果package.json有依赖，就不再检查其他来源
            except subprocess.CalledProcessError as e:
                raise RunningError(f"Failed to install some dependencies: {e}")

    # 检查是否有requirements.txt在同一目录
    req_file = os.path.join(os.path.dirname(module_path), "requirements.txt")
    if os.path.exists(req_file):
        print(
            f"• [yellow]Found requirements.txt, installing dependencies...[/]"
        )
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", req_file]
            )
            print(
                f"• [green]Dependencies installed successfully![/]"
            )
        except subprocess.CalledProcessError as e:
            raise RunningError(f"Failed to install some dependencies: {e}")


def show_package_info(self, args):
    """显示包信息"""
    if len(args) < 2:
        print(f"Error: [red]No package specified.[/]")
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
            print(f"Error: [red]Package '{pkg_name}' not found.[/]")
            self.error_code = ErrorCodeManager().get_code(FileNotFoundError)
            return

        print(f"Package: [cyan]{pkg_name}[/]")
        print(f"Type: [yellow]Single file[/]")
        return

    # 读取package.json
    package_info = read_package_info(pkg_dir)
    if not package_info:
        print(f"Package: [cyan]{pkg_name}[/]")
        print(f"Type: [yellow]Directory (no package.json)[/]")
        return

    # 显示包信息
    print(
        f"Package: [cyan]{package_info.get('command', pkg_name)}[/]"
    )
    print(
        f"Version: [green]{package_info.get('version', 'unknown')}[/]"
    )
    print(
        f"Version Code: [green]{package_info.get('version_code', 'unknown')}[/]"
    )
    print(
        f"Category: [blue]{package_info.get('category', 'Other')}[/]"
    )

    if "description" in package_info:
        print(f"Description: {package_info['description']}")

    if "author" in package_info:
        print(f"Author: [blue]{package_info['author']}[/]")

    if "dependencies" in package_info:
        print("Dependencies:")
        for dependence in sorted(package_info["dependencies"]):
            print(f"- [yellow]{dependence}[/]")


def remove_app(self, args):
    """移除已安装应用"""
    if self.NEED_PASSWD:
        auth_passwd(self)
    
    if len(args) < 2:
        print(f"Error: [red]No app name specified for removal.[/]")
        print(f"Usage: remove <app_name>")
        self.error_code = ErrorCodeManager().get_code(SyntaxError)
        return

    app_name = args[1]

    # 查找包目录
    pkg_dir = os.path.join("cmdList", "third_party", app_name)
    if not os.path.exists(pkg_dir):
        pkg_file = os.path.join("cmdList", "third_party", f"{app_name}.py")
        if not os.path.exists(pkg_file):
            raise FileNotFoundError(f"Package '{app_name}' not found.")
            return
        return

    # 读取package.json
    package_info = read_package_info(pkg_dir)
    if not package_info:
        print(f"Package: [cyan]{app_name}[/]")
        print(f"Type: [yellow]Directory (no package.json)[/]")
        return

    category = package_info.get("category", "Other")

    if app_name not in commands["commands"][category]:
        print(f"Error: [red]App '{app_name}' is not installed.[/]")
        return

    only_app = False

    try:
        # 从配置中移除
        if (
            len(commands["commands"][category]) <= 1
            and commands["commands"][category][0] == app_name
        ):
            only_app = True
        commands["commands"][category].remove(app_name)
        if only_app:
            del commands["commands"][category]

        # 删除命令文件或目录
        third_party_dir = os.path.join("cmdList", "third_party")
        py_file = os.path.join(third_party_dir, f"{app_name}.py")
        app_dir = os.path.join(third_party_dir, app_name)

        if os.path.exists(py_file):
            os.remove(py_file)
            print(
                f"• [green]App '{app_name}' removed successfully![/]"
            )
        elif os.path.exists(app_dir):
            shutil.rmtree(app_dir)
            print(
                f"• [green]App '{app_name}' removed successfully![/]"
            )
        else:
            print(
                f"Warning: [yellow]Could not find app files, but removed from configuration.[/]"
            )

        # 保存配置
        with open(os.path.join("configs", "commands.json"), "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4)

    except Exception as e:
        raise RunningError(f"Error removing app: {e}")


def list_apps(self, args):
    """列出所有已安装的第三方应用"""
    print("[on blue] Installed Apps [/]")
    categorized_apps = {}

    # 遍历所有第三方命令目录
    third_party_dir = os.path.join("cmdList", "third_party")
    if not os.path.exists(third_party_dir):
        print(f"[yellow]No third-party apps installed.[/]")
        return

    for item in os.listdir(third_party_dir):
        if item.endswith(".py") or os.path.isdir(os.path.join(third_party_dir, item)):
            cmd_name = item[:-3] if item.endswith(".py") else item
            package_json = os.path.join(third_party_dir, cmd_name, "package.json")
            category = "Other"  # 默认分类

            # 读取 package.json 获取分类
            if os.path.exists(package_json):
                try:
                    with open(package_json, "r", encoding="utf-8") as f:
                        package_info = json.load(f)
                        category = package_info.get("category", "Other")
                except (json.JSONDecodeError, IOError):
                    print(
                        f"[yellow]Warning: Invalid package.json for '{cmd_name}'[/]"
                    )

            # 将命令归类
            if category not in categorized_apps:
                categorized_apps[category] = []
            categorized_apps[category].append(cmd_name)

    # 打印分类和命令
    if not categorized_apps:
        print("[yellow]No third-party apps installed.[/]")
        return

    for category, apps in categorized_apps.items():
        print(f"{category}:")
        for app in sorted(apps):
            app_path = os.path.join(third_party_dir, f"{app}.py")
            if os.path.exists(app_path):
                print(f"- [blue]{app}[/] (single file)")
            else:
                print(f"- [blue]{app}[/] (package)")