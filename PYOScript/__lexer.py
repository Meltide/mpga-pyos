from enum import Enum, auto
from collections import deque

class TokenType(Enum):
    # 特殊标记
    AT = auto()           # @
    SLASH = auto()        # /
    SEMICOLON = auto()    # ;
    EQUAL = auto()        # =
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    BACKTICK = auto()     # `
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    PLUS = auto()         # +
    MINUS = auto()        # -
    STAR = auto()         # *
    DOT = auto()          # .
    PERCENT = auto()      # %
    CARET = auto()        # ^
    EXP = auto()          # 幂运算 (**)
    
    # 关键字
    USING = auto()        # using
    PYCODE = auto()       # PyCode
    PYTYPE = auto()       # pytype
    READER = auto()       # reader
    INT = auto()          # int
    FLOAT = auto()        # float
    STRING = auto()       # string
    BOOL = auto()         # bool
    
    # 字面量
    IDENTIFIER = auto()   # 变量名
    STRING_LITERAL = auto()  # 字符串值
    NUMBER = auto()       # 数字值
    BOOLEAN = auto()      # true/false
    
    # 注释
    COMMENT = auto()      # 单行注释
    MULTILINE_COMMENT = auto()  # 多行注释
    
    # 代码块
    CODE_BLOCK = auto()   # Python代码块内容
    
    # 其他
    NEWLINE = auto()      # 换行
    EOF = auto()          # 文件结束
    ERROR = auto()        # 错误标记

class Token:
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}, {self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.errors = []
        self.block_stack = deque()
        
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
        
        self.escape_map = {
            'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f',
            '"': '"', "'": "'", '\\': '\\'
        }

        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '^': TokenType.CARET,
            '%': TokenType.PERCENT,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '**': TokenType.EXP
        }
    
    def tokenize(self):
        """主词法分析函数"""
        while self.position < len(self.source):
            current_char = self.source[self.position]
            
            if self.in_code_block():
                self.process_block_content()
                continue
                
            if current_char in ' \t':
                self.advance()
                continue
                
            if current_char == '\n':
                self.add_token(TokenType.NEWLINE, '\n')
                self.advance()
                self.line += 1
                self.column = 1
                continue
                
            if current_char == '#':
                self.process_comment()
                continue
                
            if current_char in ('"', "'"):
                self.process_string()
                continue
                
            if current_char == '@':
                self.process_at_command()
                continue
                
            if current_char == '/':
                self.process_slash_command()
                continue
                
            if current_char in '+-*/%^()=':
                self.process_operator(current_char)
                continue
                
            if current_char == '{':
                self.process_block_start()
                continue
                
            if current_char == '}':
                self.process_block_end()
                continue
                
            if current_char.isalpha() or current_char == '_':
                self.process_identifier()
                continue
                
            if current_char.isdigit() or (current_char == '.' and self.peek().isdigit()):
                self.process_number()
                continue
                
            if current_char == ';':
                self.add_token(TokenType.SEMICOLON, ';')
                self.advance()
                continue
                
            if current_char == '`':
                self.add_token(TokenType.BACKTICK, '`')
                self.advance()
                continue
                
            self.add_error(f"Unexpected character: {current_char!r}")
            self.advance()
        
        self.check_unclosed_blocks()
        self.add_token(TokenType.EOF, '')
        return self.tokens

    def add_token(self, type_: TokenType, value: str, line: int = None, column: int = None):
        """添加token到结果列表（增强版）"""
        line = line if line is not None else self.line
        column = column if column is not None else self.column
        self.tokens.append(Token(type_, value, line, column))

    def advance(self, n=1):
        """移动到下一个字符"""
        self.position += n
        self.column += n
    
    def peek(self, n=1):
        """查看前面n个字符而不移动位置"""
        return self.source[self.position:self.position+n]
    
    def add_error(self, message):
        """记录错误"""
        error_msg = f"LexerError at {self.line}:{self.column} - {message}"
        self.errors.append(error_msg)
        self.add_token(TokenType.ERROR, error_msg)
    
    def has_error(self):
        """检查是否有错误"""
        return bool(self.errors)
    
    def in_code_block(self):
        """是否在代码块中"""
        return bool(self.block_stack)
    
    def check_unclosed_blocks(self):
        """检查未闭合的代码块"""
        while self.block_stack:
            line, col, _ = self.block_stack.pop()
            self.add_error(f"Unclosed block starting at {line}:{col}")

    def process_comment(self):
        """处理单行注释"""
        start_pos = self.position
        while self.position < len(self.source) and self.source[self.position] != '\n':
            self.advance()
        comment = self.source[start_pos:self.position]
        self.add_token(TokenType.COMMENT, comment)

    def process_string(self):
        """处理字符串字面量"""
        quote_char = self.source[self.position]
        start_line = self.line
        start_column = self.column
        self.advance()  # 跳过引号
        
        result = []
        escape = False
        
        while self.position < len(self.source):
            current_char = self.source[self.position]
            
            if current_char == '\n' and not escape:
                self.add_error(f"Unterminated string at {start_line}:{start_column}")
                return
                
            if current_char == '\\' and not escape:
                escape = True
                self.advance()
                continue
                
            if escape:
                result.append(self.escape_map.get(current_char, f'\\{current_char}'))
                escape = False
            elif current_char == quote_char:
                self.advance()
                self.add_token(TokenType.STRING_LITERAL, ''.join(result), start_line, start_column)
                return
            else:
                result.append(current_char)
            
            self.advance()
        
        self.add_error(f"Unclosed string at {start_line}:{start_column}")

    def process_multiline_string(self):
        """处理多行字符串"""
        start_line = self.line
        start_column = self.column
        self.advance(3)  # 跳过"""
        
        result = []
        while self.position + 2 < len(self.source):
            if self.peek(3) == '"""':
                self.advance(3)
                self.add_token(TokenType.MULTILINE_COMMENT, ''.join(result), start_line, start_column)
                return
                
            current_char = self.source[self.position]
            if current_char == '\n':
                result.append('\n')
                self.line += 1
                self.column = 1
            else:
                result.append(current_char)
                self.column += 1
            self.advance()
        
        self.add_error(f"Unclosed multiline string at {start_line}:{start_column}")

    def process_at_command(self):
        """处理@指令"""
        self.advance()  # 跳过@
        command = self.extract_identifier()
        self.add_token(TokenType.AT, f'@{command}')
        
        # 处理参数
        while self.position < len(self.source) and self.source[self.position] not in ';\n':
            current_char = self.source[self.position]
            
            if current_char in ' \t':
                self.advance()
                continue
                
            if current_char in ('"', "'"):
                self.process_string()
                continue
                
            if current_char.isalpha():
                word = self.extract_identifier().lower()
                if word in ('true', 'false'):
                    self.add_token(TokenType.BOOLEAN, word)
                    continue
                    
            if current_char.isdigit() or current_char == '.':
                self.process_number()
                continue
                
            self.add_error(f"Unexpected character '{current_char}' in @{command}")
            break

        # 处理结束符
        if self.position < len(self.source) and self.source[self.position] == ';':
            self.add_token(TokenType.SEMICOLON, ';')
            self.advance()

    def process_operator(self, op: str):
        """处理运算符"""
        if op == '*' and self.peek() == '*':
            self.add_token(TokenType.EXP, '**')
            self.advance(2)
            return
            
        if op in self.operators:
            self.add_token(self.operators[op], op)
            self.advance()
        else:
            self.add_error(f"Unknown operator: {op}")

    def process_block_start(self):
        """处理代码块开始"""
        self.block_stack.append((self.line, self.column, self.position))
        self.add_token(TokenType.LBRACE, '{')
        self.advance()

    def process_block_end(self):
        """处理代码块结束"""
        if not self.block_stack:
            self.add_error("Unexpected '}' without matching '{'")
            self.advance()
            return
            
        line, col, start_pos = self.block_stack.pop()
        content = self.source[start_pos+1:self.position].strip()
        
        if content:
            # 规范化缩进
            lines = content.split('\n')
            base_indent = len(lines[0]) - len(lines[0].lstrip()) if lines else 0
            normalized = '\n'.join(line[base_indent:] if len(line) > base_indent else line.lstrip() 
                         for line in lines)
            self.add_token(TokenType.CODE_BLOCK, normalized, line, col + base_indent)
        
        self.add_token(TokenType.RBRACE, '}')
        self.advance()

    def process_block_content(self):
        """处理代码块内容"""
        self.process_block_end()  # 复用代码块结束逻辑

    def process_identifier(self):
        """处理标识符"""
        start = self.position
        while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            self.advance()
        
        ident = self.source[start:self.position]
        token_type = self.keywords.get(ident, TokenType.IDENTIFIER)
        self.add_token(token_type, ident)

    def process_number(self):
        """处理数字字面量"""
        start = self.position
        has_decimal = False
        
        while self.position < len(self.source):
            current_char = self.source[self.position]
            if current_char.isdigit():
                self.advance()
            elif current_char == '.' and not has_decimal:
                has_decimal = True
                self.advance()
            else:
                break
        
        num_str = self.source[start:self.position]
        if has_decimal and (num_str.startswith('.') or num_str.endswith('.')):
            self.add_error(f"Invalid number format: {num_str}")
        else:
            self.add_token(TokenType.NUMBER, num_str)

    def process_slash_command(self):
        """处理/命令"""
        self.advance()  # 跳过/
        command = self.extract_identifier()
        self.add_token(TokenType.SLASH, f'/{command}')
        
        # 处理参数
        while self.position < len(self.source) and self.source[self.position] not in '\n#;':
            current_char = self.source[self.position]
            
            if current_char in ' \t':
                self.advance()
                continue
                
            if current_char in ('"', "'"):
                self.process_string()
                continue
                
            if current_char in '+-*/%^()=':
                self.process_operator(current_char)
                continue
                
            if current_char.isalpha() or current_char == '_':
                self.process_identifier()
                continue
                
            if current_char.isdigit() or current_char == '.':
                self.process_number()
                continue
                
            self.advance()

    def extract_identifier(self):
        """提取标识符"""
        start = self.position
        while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            self.advance()
        return self.source[start:self.position]