STRING_START = "STRING_START"
STRING_END = "STRING_END"
STRING = "STRING"
PYCODE_START = "PYCODE_START"
PYCODE_END = "PYCODE_END"
PYCODE = "PYCODE"

IN_COMMENT = (STRING, STRING_START)
IN_PYCODE = (STRING, PYCODE_START)


class PST:
    def __init__(self, type_, text, parent=None):
        """PYOScript Token"""


class PSC:
    def __init__(self, code=""):
        """PYOScript Compiler"""
        self.code = [i for i in code.splitlines() if i.strip() != ""]
        self.ast = []
        self.tokens = []
        self.one_line = True
        self.last_type = None

        self.init_code()

    def init_code(self):
        code = []
        for line in range(len(self.code)):
            cl = self.code[line]
            strip_cl = cl.strip()
            if strip_cl.startswith('"') or strip_cl.startswith("'"):
                if self.last_type in IN_COMMENT:
                    self.one_line = True
                    self.last_type = STRING_END
                else:
                    self.one_line = False
                    self.last_type = STRING_START
                continue
            elif self.last_type in IN_COMMENT:
                self.last_type = STRING
                self.one_line = False
                continue
            elif strip_cl.endswith(
                ";"
            ):  # Python代码一般不会以分号结尾,所以这里是PYOScript代码
                self.one_line = True
                if self.last_type in IN_PYCODE:
                    if strip_cl.startswith("pytype") or strip_cl.startswith("using"):
                        self.last_type = PYCODE_START
                    if strip_cl.endswith("};"):
                        self.last_type = PYCODE_END
                    elif not (
                        strip_cl.startswith("pytype") and strip_cl.startswith("using")
                    ):
                        self.last_type = PYCODE
                else:  # 一般情况
                    continue
            else:
                code.append(cl.split("#")[0])
                continue
            code.append(cl)
        self.one_line = True
        self.last_type = None
        self.code = code


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))

    with open("./demo/t1.mcfunction", "r", encoding="utf-8") as f:
        code = f.read()
    psc = PSC(code)
    print("\n".join(psc.code))
