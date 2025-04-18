import importlib
import json
import os
import subprocess


class CommandManager:
    def __init__(self, core, cmd=""):
        self.cmd = cmd
        self.core = core

        # 加载配置文件
        with open("config.json", "r") as f:
            self.cfg = json.load(f)
            self.allcmds = self.cfg["commands"]

        self.thirds = self.allcmds["Third-party"]  # 第三方命令
        self.cmds = [cmd for category in self.allcmds.values() for cmd in category]  # 所有命令列表

    def reg(self, cmd):
        """注册命令"""
        self.cmd = cmd

    def pkg_name(self):
        """获取命令对应的包名"""
        return "cmdList.third_party." + self.cmd if self.cmd in self.thirds else "cmdList." + self.cmd

    def hasattr(self, attr):
        """检查命令模块是否具有指定属性"""
        return hasattr(self.getpkg(), attr)

    def loaded_cmd(self):
        """检查命令是否已加载"""
        return self.cmd in self.cmds

    def getpkg(self):
        """导入命令对应的模块"""
        return importlib.import_module(self.pkg_name())

    def execute(self, args=()):
        """执行命令，支持带参数"""
        if self.loaded_cmd():
            pkg_name = self.pkg_name()
            __import__(pkg_name, fromlist=["execute"]).execute(*args)
        elif self.core.runsys:
            try:
                subprocess.run([self.cmd] + list(args[1]), check=True)
            except subprocess.CalledProcessError as e:
                print(f"System command failed: {e}")
        else:
            raise ImportError(f"Command '{self.cmd}' not found or not allowed to run system commands.")


class PathManager:
    def __init__(self, core):
        self.core = core
        self.path = os.getcwd()