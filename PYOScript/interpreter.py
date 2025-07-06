from collections import deque
from enum import Enum
import re
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.err import PYOScriptError
from utils.datastruct import DataStruct

with open('PYOScript/demo/t1.mcfunction', 'r', encoding='utf-8') as f:
    DEMO_CODE = f.read()

def VAR(_types=('int','float','string','bool')):
    return re.compile(
        r'('+'|'.join(_types)+r')\s+([a-zA-Z_]\w*)\s*=\s*'
        r'('
        r'[^;"\']+|'  # 非字符串值
        r'"[^"\\]*(?:\\.[^"\\]*)*"|'  # 双引号字符串
        r"'[^'\\]*(?:\\.[^'\\]*)*'"  # 单引号字符串
        r');?'
    )

class NestType(Enum):
    PYTYPE = 1 #赋值运行
    PYCODE = 2 #直接运行

class BasicTokens(Enum):
    INT = re.compile(r"(?<!\S)-?\d+(?!\S)")
    FLOAT = re.compile(r"(?<!\S)-?\d+\.\d+(?!\S)|-?\d+\.(?!\d)|\.\d+(?!\S)")
    STRING = re.compile(r"([\"'])((?:(?<!\\)\\\1|.)*?)\1")
    BOOL = re.compile(r"(?<!\S)(True|False)(?!\S)")
    MULTI_COMMENT = re.compile(
        r'''(?<!\\)(?:'{3}[\s\S]*?'{3}|"{3}[\s\S]*?"{3})'''
    )
    #COMPLEX = re.compile(r"(?<!\S)-?\d+\.?\d*[+-]\d+\.?\d*j(?!\S)")
    #NONE = re.compile(r"(?<!\S)None(?!\S)")
    BASIC_VAR = VAR()
    SPCIAL_VAR = VAR(('reader','pytype'))
    SINGLE_COMMENT = re.compile(r'(?<![\\\'"])(#(?!\\).*?$)')
    #MULTI_COMMENT = re.compile(r'''(?<!\\)(?:'{3}|"{3})(?:(?!\1).|\n)*?\1''')
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
    ALL = re.compile(
            f"{INT.pattern}|"            # INT
            f"{FLOAT.pattern}|"          # FLOAT
            f"{STRING.pattern}|"         # STRING
            f"{BOOL.pattern}"            # BOOL
        )

TYPES = {
    BasicTokens.INT: int,
    BasicTokens.FLOAT: float,
    BasicTokens.STRING: str,
    BasicTokens.BOOL: bool,
    #BasicTokens.COMPLEX: complex,
    #BasicTokens.NONE: type(None)
}

class SpecialToken:
    def __init__(self, type: BasicTokens, name: str = None, value: str = None):
        self.type = type
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Token({self.type.name}, {self.name}, {self.value})"
    def append(self, value):
        self.value += value

class PYOScriptInterpreter:
    def __init__(self,core,code:str,path='<module>'):
        self.core = core #PyOS类
        self.nest_stack = deque()
        self.nest_type = None
        self.code = code
        self.vars = dict()
        self.path = path
        self.ds = DataStruct()

    def parse_line(self,line:str):
        '''Warning: 该函数会修改原self.code，仅适用于测试用途'''
        self.code = line
        self.parse()

    def parse(self):
        self.code = BasicTokens.COMMENT.value.sub('', self.code)  # 去掉注释
        print(self.code)
        for line,codes in enumerate(self.code.splitlines()):
            for code in self.ds.strict_split(codes,';'):
                print(code,self.vars)
                stripped = code.strip()

                if not stripped:
                    continue

                #pc = self.ds.parse_cmd(stripped)
                pc = self.parse_command(stripped+';')
                print(pc)
                if pc:
                    args = []
                    for arg in pc['args']:
                        if isinstance(arg, SpecialToken):
                            if arg.type == BasicTokens.BASIC_VAR and self.vars.get(arg.name):
                                args.append(self.vars[arg.name])
                            else:
                                raise PYOScriptError(f"Undefined variable: {arg.name}", line, self.path, 'Syntax')
                        else:
                            args.append(eval(arg))
                    self.core._register_and_execute(pc['command'], args)
                    continue

                pv = self.parse_var_decl(stripped)
                if pv:
                    var_type, var_name, var_value = self.format_var(*pv)
                    '''if not BasicTokens.ALL.value.fullmatch(var_value):
                        if self.vars.get(var_value):
                            var_value = self.vars[var_value]
                        else:
                            raise PYOScriptError(f"Undefined variable: {var_value}", line, self.path, 'Syntax')'''
                    val = self.ds.expression_evaluator(self.vars, var_value, line, self.path)
                    #print('=====',val)
                    
                    if isinstance(eval(var_type+'()'), type(val)):
                        self.vars[var_name] = val
                    else:
                        raise PYOScriptError(f"Type mismatch: {var_type} and {type(val)}", line, self.path, 'Syntax')
                    continue

                #raise PYOScriptError(f"Invalid syntax: {stripped}", line, self.path, 'Syntax')
    
    def parse_var_decl(self,line:str):
        # 匹配 int a=1 或 int a = 1 等情况
        match = BasicTokens.BASIC_VAR.value.match(line)
        if match:
            var_type = match.group(1)
            var_name = match.group(2)
            var_value = match.group(3).rstrip(';')  # 去掉结尾分号
            #print(var_type, var_name, var_value)
            return var_type, var_name, var_value
        return None

    def parse_command(self, command_str: str):
        '''与foxShell.parse_commands不同，添加了变量解析'''
        # 主正则表达式（保持原有结构）

        match = BasicTokens.CMD.value.fullmatch(command_str)
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
                    result['args'].append(SpecialToken(BasicTokens.BASIC_VAR, var_name))
        
        return result
    def format_var(self, _type, _name, _value):
        ftype = {
            'string':'str'
        }
        fvalue = {
            'true':'True',
            'false':'False'
        }
        return ftype.get(_type, _type) ,_name ,fvalue.get(_value, _value)
    
if __name__ == '__main__':
    from pyos import PyOS
    test_os = PyOS(debug=True)
    interpreter = PYOScriptInterpreter(test_os,DEMO_CODE)
    interpreter.parse()