from cmdList.registerCmd import registerCmd
import sys #系统底层库

def exit(self):
    self.error = 0
    self.clear()
    sys.exit(0)

registerCmd().register("exit", "Log out", "Power", exit)