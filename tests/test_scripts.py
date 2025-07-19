"""import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PYOScript.interpreter import *
from pyos import PyOS

CODE_1 = '''
int a = 1
float b = 2.5
/echo `a` + `b`
'''

class TestScripts:
    def test_code(self):
        core = PyOS(debug=True)
        ip = PYOScriptInterpreter(core, CODE_1)
        ip.parse()
        ip.parse_line('/echo hi')"""