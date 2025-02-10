from colorama import Fore,Back
from textwrap import fill

__doc__="Get the command list"

allcmds={
    "System":['ls','version','clear','neofetch','userman','hostman'],
    "Tools":['time','calendar','calc','asciier'],
    "Games":['numgame','finguess'],
    "Power":['exit','shutdown','restart']
}

def execute(self,args):
    if not args:
        print("Available commands:")
        for types,cmds in allcmds.items():
            print(Back.BLUE+types)
            for cmd in cmds:
                doc=__import__("cmdList."+cmd, fromlist=["__doc__"]).__doc__
                print(f"{cmd:<20} {doc}")
    else:
        cmd=args[0]
        if cmd in cmds:
            print(cmd+":",__import__("cmdList."+cmd, fromlist=["__doc__"]).__doc__)
        else:
            print(Fore.RED+"help: Command not found")