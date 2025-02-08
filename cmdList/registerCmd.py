class registerCmd:
    cmdList = {}
    shallowCmd = {}

    def register(self, cmdName: str, desc: str, category: str, callback):
        if registerCmd.cmdList.get(category, False) == False:
            registerCmd.cmdList[category] = {}
            registerCmd.cmdList[category][cmdName] = [desc, callback]
        else:
            registerCmd.cmdList[category][cmdName] = [desc, callback]

        registerCmd.shallowCmd[cmdName] = callback

    def getCmdList(self) -> dict:
        return registerCmd.cmdList