from cmdList.registerCmd import registerCmd

def clear(self):
    self.error = 0
    self.clear()

registerCmd().register("clear", "Clean the screen", "System", clear)