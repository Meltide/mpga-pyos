from enum import Enum, auto
import re

class LexerError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Line {line}:{column} - {message}" if line else message)

class TokenType(Enum):
    # 特殊标记
    AT = auto()           # @
    SLASH = auto()        # /
    SEMICOLON = auto()    # ;
    EQUAL = auto()        # =
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    BACKTICK = auto()     # `
    
    # 关键字
    USING = auto()        # using
    PYCODE = auto()       # PyCode
    PYTYPE = auto()       # pytype
    READER = auto()       # reader
    INT = auto()          # int
    FLOAT = auto()        # float
    STRING = auto()       # string
    BOOL = auto()        # bool
    
    # 字面量
    IDENTIFIER = auto()  # 变量名/命令名等
    STRING_LITERAL = auto()  # 字符串值
    NUMBER = auto()      # 数字值
    BOOLEAN = auto()     # true/false
    
    # 注释
    COMMENT = auto()     # 单行注释
    MULTILINE_COMMENT = auto()  # 多行注释
    
    # 其他
    NEWLINE = auto()     # 换行
    EOF = auto()         # 文件结束
    ERROR = auto()  # 用于错误token

class Token:
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}, {self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # 关键字映射
        self.keywords = {
            'using': TokenType.USING,
            'PyCode': TokenType.PYCODE,
            'pytype': TokenType.PYTYPE,
            'reader': TokenType.READER,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING,
            'bool': TokenType.BOOL,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
        }
    
    def tokenize(self):
        self.errors = []
        while self.position < len(self.source):
            try:
                current_char = self.source[self.position]
                
                # 跳过空白字符
                if current_char in ' \t':
                    self.advance()
                    continue
                    
                # 处理换行
                if current_char == '\n':
                    self.add_token(TokenType.NEWLINE, '\n')
                    self.advance()
                    self.line += 1
                    self.column = 1
                    continue
                    
                # 处理单行注释
                if current_char == '#':
                    comment = self.extract_until('\n')
                    self.add_token(TokenType.COMMENT, comment)
                    continue
                    
                # 处理多行注释/字符串
                if current_char == '"':
                    if self.source[self.position:self.position+3] == '"""':
                        # 多行注释/字符串
                        content = self.extract_multiline_string()
                        self.add_token(TokenType.MULTILINE_COMMENT, content)
                    else:
                        # 单行字符串
                        content = self.extract_string()
                        self.add_token(TokenType.STRING_LITERAL, content)
                    continue
                    
                # 处理@符号开头的指令
                if current_char == '@':
                    self.process_at_command()
                    continue
                    
                # 处理/开头的命令
                if current_char == '/':
                    self.process_slash_command()
                    continue
                    
                # 处理变量声明和赋值
                if current_char.isalpha() or current_char == '_':
                    identifier = self.extract_identifier()
                    token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)
                    self.add_token(token_type, identifier)
                    continue
                    
                # 处理数字
                if current_char.isdigit() or (current_char == '.' and self.position + 1 < len(self.source) and self.source[self.position+1].isdigit()):
                    number = self.extract_number()
                    self.add_token(TokenType.NUMBER, number)
                    continue
                    
                # 处理符号
                if current_char == ';':
                    self.add_token(TokenType.SEMICOLON, ';')
                    self.advance()
                    continue
                    
                if current_char == '=':
                    self.add_token(TokenType.EQUAL, '=')
                    self.advance()
                    continue
                    
                if current_char == '{':
                    self.add_token(TokenType.LBRACE, '{')
                    self.advance()
                    continue
                    
                if current_char == '}':
                    self.add_token(TokenType.RBRACE, '}')
                    self.advance()
                    continue
                    
                if current_char == '`':
                    self.add_token(TokenType.BACKTICK, '`')
                    self.advance()
                    continue
                    
                # 未知字符
                self.advance()
            except LexerError as e:
                self.errors.apprnd(str(e))
                # 尝试从错误中恢复（例如跳到下一行）
                self.recover_from_error()
        if self.errors:
            print("\nLEXER ERRORS:")
            for error in self.errors:
                print(f"- {error}")
            
        self.add_token(TokenType.EOF, '')
        return self.tokens
    def recover_from_error(self):
        """尝试跳到下一个安全点继续解析"""
        while self.position < len(self.source):
            char = self.source[self.position]
            if char in {'\n', ';'}:
                self.advance()
                return
            self.advance()
    def advance(self):
        self.position += 1
        self.column += 1
    
    def add_token(self, type_: TokenType, value: str):
        self.tokens.append(Token(type_, value, self.line, self.column))
    
    def extract_until(self, delimiter: str) -> str:
        start = self.position
        while self.position < len(self.source) and self.source[self.position] != delimiter:
            self.advance()
        result = self.source[start:self.position]
        if self.position < len(self.source) and self.source[self.position] == delimiter:
            self.advance()
        return result
    
    def extract_string(self) -> str:
        self.advance()  # 跳过开始的"
        start = self.position
        result = []
        
        while self.position < len(self.source):
            current_char = self.source[self.position]
            
            # 处理转义字符
            if current_char == '\\':
                self.advance()
                if self.position >= len(self.source):
                    self.add_token(TokenType.ERROR, "Unterminated escape sequence")
                    return ""
                    
                escape_char = self.source[self.position]
                # 支持常见转义序列
                if escape_char == 'n':
                    result.append('\n')
                elif escape_char == 't':
                    result.append('\t')
                elif escape_char in ('"', '\\'):
                    result.append(escape_char)
                else:
                    result.append('\\' + escape_char)
                self.advance()
                continue
                
            # 结束引号
            elif current_char == '"':
                self.advance()
                return ''.join(result)
                
            # 普通字符
            else:
                result.append(current_char)
                self.advance()
        
        # 如果执行到这里说明没有遇到闭合引号
        self.add_token(TokenType.ERROR, f"Unclosed string literal starting at line {self.line}")
        return ''.join(result)
    
    def extract_multiline_string(self) -> str:
        self.position += 3  # 跳过开始的"""
        start_pos = self.position
        start_line = self.line
        result = []
        
        while self.position + 2 < len(self.source):
            current_char = self.source[self.position]
            
            # 处理转义字符（与单行字符串相同）
            if current_char == '\\':
                self.advance()
                if self.position >= len(self.source):
                    self.add_token(TokenType.ERROR, "Unterminated escape sequence")
                    return ""
                # ... (与单行字符串相同的转义处理逻辑)
            
            # 检查结束标记
            if (current_char == '"' and 
                self.position + 2 < len(self.source) and
                self.source[self.position+1] == '"' and 
                self.source[self.position+2] == '"'):
                self.position += 3
                return ''.join(result)
                
            # 处理换行
            if current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
                
            result.append(current_char)
            self.position += 1
        
        # 未闭合错误
        self.add_token(TokenType.ERROR, 
                    f"Unclosed multi-line string starting at line {start_line}")
        return ''.join(result)
    
    def extract_identifier(self) -> str:
        start = self.position
        while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            self.advance()
        return self.source[start:self.position]
    
    def extract_number(self) -> str:
        start = self.position
        has_decimal = False
        
        while self.position < len(self.source):
            if self.source[self.position].isdigit():
                self.advance()
            elif self.source[self.position] == '.' and not has_decimal:
                has_decimal = True
                self.advance()
            else:
                break
        
        return self.source[start:self.position]
    
    def process_at_command(self):
        self.advance()  # 跳过@
        command = self.extract_identifier()
        self.add_token(TokenType.AT, '@' + command)
        
        # 读取后面的字符串值
        while self.position < len(self.source) and self.source[self.position] in ' \t':
            self.advance()
            
        if self.position < len(self.source) and self.source[self.position] == '"':
            value = self.extract_string()
            self.add_token(TokenType.STRING_LITERAL, value)
        
        # 确保分号
        while self.position < len(self.source) and self.source[self.position] in ' \t':
            self.advance()
            
        if self.position < len(self.source) and self.source[self.position] == ';':
            self.add_token(TokenType.SEMICOLON, ';')
            self.advance()
    
    def process_slash_command(self):
        self.advance()  # 跳过/
        command = self.extract_identifier()
        self.add_token(TokenType.SLASH, '/' + command)
        
        # 处理命令参数
        while self.position < len(self.source) and self.source[self.position] != '\n':
            current_char = self.source[self.position]
            
            if current_char in ' \t':
                self.advance()
                continue
                
            if current_char == '#':  # 命令后的注释
                comment = self.extract_until('\n')
                self.add_token(TokenType.COMMENT, comment)
                break
                
            # 其他参数处理
            self.advance()

def test_lexer():
    source = '''
    @name "demo\\n1.0";
    str = "unclosed
    str2 = "with escape\\"";
    """
    multi
    line\\n
    """
    '''
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    # 输出token流
    for token in tokens:
        if token.type != TokenType.ERROR:
            print(f"{token.line}:{token.column} {token.type.name:15} {token.value!r}")

    # 输出错误
    if lexer.errors:
        print("\nERRORS:")
        for error in lexer.errors:
            print(error)

if __name__ == '__main__':
    test_lexer()