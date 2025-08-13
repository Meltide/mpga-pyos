from collections import deque

class TokenType:
    def __init__(self, value: str, description: str = '', **kwargs):
        self.value = value
        self.description = description
        self.highlight = 'default'
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return f'TokenType({self.value!r})'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

class Strip(TokenType):
    def __repr__(self):
        return f'Strip({self.value!r})'
    
class Info(TokenType):
    def __repr__(self):
        return f'Info({self.value!r})'
    
class String(TokenType):
    def __repr__(self):
        return f'String({self.value!r})'
   
class Others(TokenType):
    def __repr__(self):
        return f'Others({self.value!r})'

class Number(TokenType):
    def __repr__(self):
        return f'Number({self.value!r})'

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.tokens = deque()
        self.stack = deque()
        self.area = None

    def tokenize(self):
        lines = self.code.splitlines()
        keepend_lines = self.code.splitlines(keepends=True)
        for i in range(len(keepend_lines)):
            line = lines[i]
            '''if line.startswith('#'):
                continue  # Skip comments
            elif line.startswith('@'):

            for col in line:
                
                if line.isdigit():
                    yield Number(line)
                elif line.startswith('"') and line.endswith('"'):
                    yield String(line[1:-1])
                else:
                    yield Others(line)'''
            for col in line:
                if col in ('"', "'"):
                    if self.area == String:
                        self.area = None
                        self.tokens.append(self.stack.pop())
                    else:
                        self.area = String
                elif self.area == String:
                    self.stack.append(col)
                elif i > len(lines) - 1:
                    self.tokens.append(Strip(col, 'n'))
                    