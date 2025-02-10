import os #系统底层库

def execute(self):
    print(*os.listdir(os.getcwd()))
