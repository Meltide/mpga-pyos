from colorama import Fore

__doc__="Get the command list"

cmds=["asciier","calc","calendar","clear","exit","finguess","help","hostman","ls","neofetch","numgame","passwd","restart","shutdown","time","userman","version"]
def execute(args):
    if len(args)==0:
        print("Available commands:")
        for cmd in cmds:
            print(cmd+": "+__import__("cmdList."+cmd, fromlist=["__doc__"]).__doc__)
    else:
        cmd=args[0]
        if cmd in cmds:
            print(__import__("cmdList."+cmd, fromlist=["__doc__"]).__doc__)
        else:
            print(Fore.RED+"Command not found")