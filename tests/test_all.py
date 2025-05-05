import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import *

class Test:
    def test_errcode(self):
        '''查重测试'''
        assert len(set(EXCEPTION_RETURNS.values())) == len(EXCEPTION_RETURNS)
        assert len(set(EXCEPTION_INFO.keys())) == len(EXCEPTION_INFO)
