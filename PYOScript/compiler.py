STRING_START = 'STRING_START'
STRING_END = 'STRING_END'
STRING = 'STRING'
PYCODE_START = 'PYCODE_START'
PYCODE_END = 'PYCODE_END'
PYCODE = 'PYCODE'

IN_COMMENT = (STRING,STRING_START)
IN_PYCODE = (STRING,PYCODE_START)

class PST:
    def __init__(self,type_,text,parent=None):
        '''PYOScript Token'''

class PSC:
    def __init__(self,code=''):
        '''PYOScript Compiler'''
        self.code = [i for i in code.splitlines() if i.strip()!='']
        self.ast = []
        self.tokens = []
        self.one_line = True
        self.last_type = None

        self.init_code()

    def init_code(self):
        code=[]
        for line in range(len(self.code)):
            cl = self.code[line]
            strip_cl = cl.strip()
            if strip_cl.startswith('"') or strip_cl.startswith("'"):
                if self.last_type in IN_COMMENT:
                    self.one_line=True
                    self.last_type=STRING_END
                else:
                    self.one_line=False
                    self.last_type=STRING_START
                continue
            elif self.last_type in IN_COMMENT:
                self.last_type=STRING
                self.one_line=False
                continue
            elif strip_cl.endswith(';'): #Python代码一般不会以分号结尾,所以这里是PYOScript代码
                self.one_line=True
                if self.last_type in IN_PYCODE:
                    if strip_cl.startswith('pytype') or strip_cl.startswith('using'):
                        self.last_type=PYCODE_START
                    if strip_cl.endswith('};'):
                        self.last_type=PYCODE_END
                    elif not (strip_cl.startswith('pytype') and strip_cl.startswith('using')):
                        self.last_type=PYCODE
                else: #一般情况
                    continue
            else:
                code.append(cl.split('#')[0])
                continue
            code.append(cl)
        self.one_line = True
        self.last_type = None
        self.code = code

if __name__ == '__main__':
    code='''
@author JvavLargePython #标明作者
@name demo #脚本命令名（可用作插件）
@version 1.1.4#版本号
@description A test. #描述

"""
多行
注释（字符串）
"""
/yet list; #命令
@config system_commands true; #临时调整config.json，指运行时修改文件，运行完成后恢复
/python; #系统命令
int a = 1;float b = 2.0; #基本变量用法，计划支持整数、浮点数、字符串、布尔值

using PyCode {
    import os
    print("hi")
}; #python单、多行代码运行基本用法
using PyCode {
    print(`a+`b)
}; #python单、多行代码运行赋值用法
pytype c = {
    def main():
        return `a
    main()
}; #python单、多行代码赋值用法
/echo `c; #命令运行赋值用法
reader d = ./a.py;
/runpy `d;
    '''
    psc = PSC(code)
    print('\n'.join(psc.code))
