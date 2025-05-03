__doc__="Run PYOScript files(.pyos)"

import os
from utils.config import *

class PYOScript:
    def __init__(self,core):
        self.tab=0
        self.end=True
        self.code=[]
        self.core=core
    def read(self,filename):
        with open(filename,"r") as f:
            self.code=f.read().splitlines()
    def execute(self):
        for line in self.code:
            tokens=line.split(" ")

    def run(self,code=""):
        if not code:
            self.code=[code]
        self.execute()
        
def execute(self,args):
    script=PYOScript(self)
    if os.path.isfile(args[0]):
        script.read(args[0])
    script.run()