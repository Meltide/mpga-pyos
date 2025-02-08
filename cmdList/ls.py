from cmdList.registerCmd import registerCmd
import os #系统底层库

def ls(self):
    self.error = 0
    print(*os.listdir(os.getcwd()))

registerCmd().register("ls", "View the path", "System", ls)