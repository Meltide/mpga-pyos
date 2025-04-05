import json,shutil,os
from . import help
from colorama import Fore

__doc__ = "Registry commands"

def execute(self,args):
    cfg=help.cfg
    addname=os.path.splitext(os.path.basename(args[0]))[0]
    if addname in help.cmds:
        print(Fore.RED+"Invalid command name!")
        return
    cfg["commands"]["Third-party"]+=addname
    #print(cfg)
    with open("config.json","w",encoding="utf-8") as f:
        json.dump(cfg,f,indent=4)
    try:
        shutil.copy2(args[0],"./cmdList/third_party/"+addname+".py")
        help.execute(self,addname)
        print(Fore.GREEN+"Command loaded successfully.")
    except shutil.SameFileError:
        print(Fore.YELLOW+"Command already exists.")
    except:
        print(Fore.RED+"Failed to load command help.")