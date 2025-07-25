import json, os, shutil, subprocess
from .err import *

# 导入配置文件
with open(os.path.join("configs", "profiles.json"), "r", encoding="utf-8") as f:
    profiles: dict = json.load(f)

with open(os.path.join("configs", "system_policys.json"), "r", encoding="utf-8") as f:
    policys: dict = json.load(f)

with open(os.path.join("configs", "commands.json"), "r", encoding="utf-8") as f:
    commands: dict = json.load(f)

# profiles.json
HOSTNAME: str = profiles["hostname"]
ACCOUNTS: dict = profiles["accounts"]
ACCOUNT_NAMES: list = ACCOUNTS.keys()
GROUPS: list = profiles["groups"]
AUTO_LOGIN: str = profiles["auto_login"]

# system_policys.json
SHOW_BASE_ERROR_DETAILS: bool = policys["show_base_error_details"]
SHOW_AD: bool = policys["show_ad"]
USE_CUSTOM_STARTUPMSG: bool = policys["use_custom_startupmsg"]

# commands.json
SIGNED_COMMANDS: dict = commands["commands"]
SC_SYSTEM: list = SIGNED_COMMANDS["System"]
SC_TOOLS: list = SIGNED_COMMANDS["Tools"]
SC_POWER: list = SIGNED_COMMANDS["Power"]

# 其他
BASEPATH: str = os.getcwd().replace("\\", "/")


# 重载 FoxShell
def reload_fox():
    with open(os.path.join("configs", "Fox", "config.json"), "r", encoding="utf-8") as f:
        fox: dict = json.load(f)


EXCEPTION_INFO: dict = {119: "Unknown command."}

EXCEPTION_RETURNS: dict = {
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
    UnboundLocalError: 149,
    LookupError: 156,
    ReferenceError: 164,
    shutil.SameFileError: 170,
    shutil.SpecialFileError: 171,
    shutil.ExecError: 172,
    shutil.Error: 173,
    shutil.ReadError: 174,
    os.error: 176,
    subprocess.CalledProcessError: 177,
    subprocess.TimeoutExpired: 178,
    subprocess.SubprocessError: 179,

    # 自定义错误码
    RunningError: 810, 
    PYOScriptError: 191,
}
