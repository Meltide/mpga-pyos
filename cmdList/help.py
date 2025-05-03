from colorama import Fore,Back
import json
from utils.man import CommandManager

__doc__="Get the command list"

def execute(self,args):
    cmdman=CommandManager(self)
    if not args:
        print("Available commands:")
        for types,cmds in cmdman.allcmds.items():
            print(Back.BLUE+" "+types+" ")
            for cmd in cmds:
                cmdman.reg(cmd)
                doc=cmdman.getpkg().__doc__
                print(f"{cmd:<20} {doc}")
    else:
        cmd=args[0]
        cmdman.reg(cmd)
        if cmdman.loaded_cmd():
            print(cmd+":",cmdman.getpkg().__doc__)
            if cmdman.hasattr("__usage__"):
                print(Back.BLUE+" Usage of "+cmd+" ")
                for usage,desc in cmdman.getpkg().__usage__.items():
                    print(f"{cmd} {usage:<20} {desc}")
        else:
            print(Fore.RED+"help: Command not found")