import time

__doc__ = "Show the time and date"

def execute(self, args):
    other_StyleTime = time.strftime("%Y-%m-%d %H:%M:%S")
    print(other_StyleTime)
