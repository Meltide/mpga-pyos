class RunningError(Exception):
    def __init__(self, message="Invalid command."):
        self.message = message

    def __str__(self):
        return self.message

class PYOScriptError(SyntaxError):
    def __init__(self, message=None, line_no=0, path='<module>', type_=''):
        self.message = message
        self.line = line_no
        self.path = path
        self.type_ = type_

    def __str__(self):
        return f"PYOScript{self.type_}Error: {self.message} (at line {self.line}, in {self.path})"