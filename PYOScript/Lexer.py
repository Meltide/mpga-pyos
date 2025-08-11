from collections import deque

class TokenType:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f'TokenType({self.value!r})'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

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

    def tokenize(self):
        for line in self.code.splitlines():
            if line.startswith('#'):
                continue  # Skip comments
            if line.isdigit():
                yield Number(line)
            elif line.startswith('"') and line.endswith('"'):
                yield String(line[1:-1])
            else:
                yield Others(line)