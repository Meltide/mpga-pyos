from cmdList.registerCmd import registerCmd
from colorama import Back #彩色文字库

def help(self):
    cmdList = registerCmd().getCmdList()
    for i in range(len(cmdList)):
        category = list(cmdList.keys())
        sameCategoryCmd = list(cmdList.values())
        if category[i] != "None":
            print(f"{Back.BLUE} {category[i]} ")
        else:
            continue
        for j in range(len(sameCategoryCmd[i])):
            cmdName: str = list(dict(sameCategoryCmd[i]).keys())[j]
            cmdDesc: str = list(dict(sameCategoryCmd[i]).values())[j][0]
            print(f"{cmdName.ljust(12)}{cmdDesc}")


registerCmd().register("help", "Get the command list", "None", help)