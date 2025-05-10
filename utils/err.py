class RunningError(Exception):
    '''未知运行错误'''
    def __init__(self, message="Invalid command."):
        self.message = message

    def __str__(self):
        return self.message