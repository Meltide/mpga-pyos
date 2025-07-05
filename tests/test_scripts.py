import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PYOScript.interpreter import *
from pyos import PyOS

class TestScripts:
    def test_code(self):
        core = PyOS()
        ip = PYOScriptInterpreter(core,DEMO_CODE)
        ip.parse()
        ip.parse_line('/echo hi')