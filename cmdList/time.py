from cmdList.registerCmd import registerCmd
import time

def Time(self):
    self.error = 0
    other_StyleTime = time.strftime("%Y-%m-%d %H:%M:%S")
    print(other_StyleTime)

registerCmd().register("time", "Show the time and date", "Tools", Time)