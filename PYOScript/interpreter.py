import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import Lexer

with open('PYOScript/demo/t1.mcfunction', 'r', encoding='utf-8') as f:
    DEMO_CODE = f.read()

class PYOScriptInterpreter:
    def __init__(self):
        for token in Lexer(DEMO_CODE).tokenize():
            print(token)

if __name__ == '__main__':
    interpreter = PYOScriptInterpreter()