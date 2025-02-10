import os #系统底层库
__doc__="View the path"
def execute(self,args):
    print(*os.listdir(os.getcwd()))
