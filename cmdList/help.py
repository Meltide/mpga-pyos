from colorama import Fore,Back
import json

__doc__="Get the command list"

with open("config.json","r") as f:
    cfg=json.load(f)
    allcmds=cfg["commands"]
thirds=allcmds["Third-party"]

def execute(self,args):
    if not args:
        print("Available commands:")
        for types,cmds in allcmds.items():
            print(Back.BLUE+" "+types+" ")
            for cmd in cmds:
                doc=__import__("cmdList.third_party."+cmd if cmd in thirds else "cmdList."+cmd, fromlist=["__doc__"]).__doc__
                print(f"{cmd:<20} {doc}")
    else:
        cmd=args[0]
        cmds=[cmd for category in allcmds.values() for cmd in category]
        if cmd in cmds:
            print(cmd+":",__import__("cmdList.third_party."+cmd if cmd in thirds else "cmdList."+cmd, fromlist=["__doc__"]).__doc__)
        else:
            print(Fore.RED+"help: Command not found")