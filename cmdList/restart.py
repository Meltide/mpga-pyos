from cmdList.registerCmd import registerCmd

def restart(self):
    self.error = 0
    self.clear()
    PyOS()

registerCmd().register("restart", "Restart PyOS", "Power", restart)