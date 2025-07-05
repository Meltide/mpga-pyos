from collections import deque
from enum import Enum
import re

class BasicTokens(Enum):
    INT = re.compile(r"(?<!\S)-?\d+(?!\S)")
    FLOAT = re.compile(r"(?<!\S)-?\d+\.\d+(?!\S)|-?\d+\.(?!\d)|\.\d+(?!\S)")
    STRING = re.compile(r"([\"'])((?:(?<!\\)\\\1|.)*?)\1")
    BOOL = re.compile(r"(?<!\S)(True|False)(?!\S)")
    #COMPLEX = re.compile(r"(?<!\S)-?\d+\.?\d*[+-]\d+\.?\d*j(?!\S)")
    #NONE = re.compile(r"(?<!\S)None(?!\S)")
    VAR = re.compile(r'(int|float|string|bool|pytype)\s+([a-zA-Z_]\w*)\s*=\s*(.+)')
    SINGLE_COMMENT = re.compile(r'(?<![\\\'"])(#(?!\\).*?$)')
    MULTI_COMMENT = re.compile(r'''(?<!\\)(?:'{3}|"{3})(?:(?!\1).|\n)*?\1''')
    COMMENT = re.compile(f'(?ms)({SINGLE_COMMENT.pattern})|({MULTI_COMMENT.pattern})')
    CMD = re.compile(r'''
            ^/
            (?P<command>[a-zA-Z_]\w*)
            (?:
                \s+
                (?P<args>
                    (?:
                        [^;\s"']+
                        |
                        "(?:\\.|[^"\\])*"
                        |
                        '(?:\\.|[^'\\])*'
                        |
                        `[^`]+`
                    )+
                )
            )?
            ;$
        ''', re.VERBOSE)

    @property
    def ALL(self):
        # 简单组合所有模式
        return re.compile(
            f"{self.INT.value.pattern}|"            # INT
            f"{self.FLOAT.value.pattern}|"          # FLOAT
            f"{self.STRING.value.pattern}|"         # STRING
            f"{self.BOOL.value.pattern}"            # BOOL
        )

def parse_var_decl(line):
    # 匹配 int a=1 或 int a = 1 等情况
    match = BasicTokens.VAR.value.match(line)
    if match:
        var_type = match.group(1)
        var_name = match.group(2)
        var_value = match.group(3).rstrip(';')  # 去掉结尾分号
        return var_type, var_name, var_value
    return None

class SpecialToken:
    def __init__(self, type: str, name: str = None, value: str = None):
        self.type = type
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.name}, {self.value})"
    def append(self, value):
        self.value += value

class PYOScriptInterpreter:
    def __init__(self,core,code:str):
        self.core = core
        self.nest_stack = deque()
        self.nest_out = True
        self.code = code

    def parse(self):
        for line in self.code.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
    def parse_command(self,command_str:str):
        # 主正则表达式（保持原有结构）
        pattern = BasicTokens.CMD.value

        match = pattern.fullmatch(command_str.strip())
        if not match:
            return None
        
        result = {
            'command': match.group('command'),
            'args': []
        }
        
        if match.group('args'):
            # 使用辅助正则表达式分割参数（保持顺序）
            arg_pattern = re.compile(r'''
                ([^"\'\s`]+)
                |
                "((?:\\.|[^"\\])*)"
                |
                '((?:\\.|[^'\\])*)'
                |
                `([^`]+)`
            ''', re.VERBOSE)
            
            for arg_match in arg_pattern.finditer(match.group('args')):
                # 普通参数（第1组）
                if arg_match.group(1):
                    result['args'].append(arg_match.group(1))
                
                # 双引号参数（第2组）
                elif arg_match.group(2):
                    result['args'].append(f'"{arg_match.group(2)}"')
                
                # 单引号参数（第3组）
                elif arg_match.group(3):
                    result['args'].append(f"'{arg_match.group(3)}'")
                
                # 反引号参数（第4组）
                elif arg_match.group(4):
                    var_name = arg_match.group(4)
                    result['args'].append(SpecialToken('var', var_name))
        
        return result