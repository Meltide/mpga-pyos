from colorama import Fore

__doc__="Get the command list"

cmds=["asciier","calc","calendar","clear","exit","finguess","help","hostman","ls","neofetch","numgame","passwd","restart","shutdown","time","userman","version"]
def execute(self,args):
    if not args:
        print("Available commands:")
        for cmd in cmds:
            print(cmd+":",__import__("cmdList."+cmd, fromlist=["__doc__"]).__doc__)
    else:
        cmd=args[0]
        #print(cmd)
        if cmd in cmds:
            print(cmd+":",__import__("cmdList."+cmd, fromlist=["__doc__"]).__doc__)
        else:
            print(Fore.RED+"help: Command not found")