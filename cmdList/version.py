from cmdList.registerCmd import registerCmd

def version(self):
    self.error = 0
    print(f"PY OS (R) Core Open Source System {self.ver}")

registerCmd().register("version", "Show the system's version", "System", version)