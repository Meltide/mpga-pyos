__doc__="turn to a directory"

def execute(self,args):
    if not args:
        args=['']
    match args[0]:
        case "" | "~" | "home":
            self.file = "~"
        case ".." | "/":
            self.file = "/"