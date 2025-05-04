import importlib
import os
import subprocess

from .config import *
from .err import *


class CommandManager:
    def __init__(self, core, _cmd=""):
        self.cmd = _cmd
        self.core = core
        self.allcmds = SIGNED_COMMANDS  # 所有命令
        self.thirds = SC_THIRD_PARTY  # 第三方命令
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
        elif ALLOW_SYSTEM_COMMANDS:
            try:
                subprocess.run([self.cmd] + list(args[1]), check=True)
            except subprocess.CalledProcessError as e:
                print(f"System command failed: {e}")
        else:
            raise ImportError(f"Command '{self.cmd}' not found or not allowed to run system commands.")


class PathManager:
    def __init__(self, core):
        self.core = core
        self.basepath = BASEPATH

    def real_to_fake(self, path:str, userspace=False):
        """将真实路径转换为虚拟路径"""
        basepath = os.path.join(self.basepath,"vm/home",self.core.account_names) if userspace else self.basepath
        assert path.startswith(basepath.replace("\\", "/")), "Path not in userspace"
        return os.path.relpath(path, basepath).replace("\\", "/")

    def fake_to_real(self, path:str, userspace=False):
        """将虚拟路径转换为真实路径"""
        basepath = os.path.join(self.basepath,"vm/home",self.core.account_names) if userspace else self.basepath
        assert path.startswith(basepath.replace("\\", "/")), "Path not in userspace"
        return os.path.join(basepath, path.replace("\\", "/"))
    
class ErrorCodeManager:
    def __init__(self):
        self.info = {
            119: "Unknown command."
        }
        self.returns = {
            FileNotFoundError: 404,
            PermissionError: 403,
            KeyError: 300,
            SystemExit: -1,
            KeyboardInterrupt: -30,
            EOFError: -31,
            Exception: 114,
            BaseException: -114,
            TypeError: 111,
            ValueError: 112,
            IndexError: 113,
            NameError: 115,
            AttributeError: 116,
            OSError: 117,
            NotImplementedError: 118,
            ImportError: 119,
            RuntimeError: 120,
            SyntaxError: 121,
            IndentationError: 122,
            TabError: 123,
            UnicodeError: 124,
            UnicodeDecodeError: 125,
            UnicodeEncodeError: 126,
            UnicodeTranslateError: 127,
            SystemError: 128,
            ZeroDivisionError: 129,
            ArithmeticError: 130,
            FloatingPointError: 131,
            OverflowError: 132,
            AssertionError: 133,
            MemoryError: 134,
            BufferError: 135,
            ReferenceError: 136,
            RecursionError: 138,
            GeneratorExit: 140,
            KeyboardInterrupt: 141,
            StopIteration: 142,
            StopAsyncIteration: 143,
            StopAsyncIteration: 146,
            LookupError: 156,
            ReferenceError: 164,

            ErrorCodeManager: 810 # 自定义错误码
        }
    def get_code(self, e):
        """获取错误码"""
        return self.returns.get(type(e),0)
    def get_type(self, code):
        """获取错误类型"""
        for k,v in self.returns.items():
            if v==code:
                return k.__name__
        return "UnknownException"
    def get_info(self, code_or_e):
        """获取错误信息"""
        if isinstance(code_or_e,int):
            return self.info.get(code_or_e,self.get_type(code_or_e))
        else:
            return self.info.get(self.get_code(code_or_e),type(code_or_e).name)