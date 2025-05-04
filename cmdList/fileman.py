__doc__='File manager'
__usage__={
    "create":"Create a new file",
    "delete":"Delete a file",
    "read":"Read a file",
    "write":"Write to a file",
    "append":"Append to a file",
    "rename":"Rename a file",
    "copy":"Copy a file",
    "move":"Move a file",
    "ls":"List files in a directory",
    "search":"Search for a file"
}

from utils.err import RunningError

def execute(self,args):
    match args[0]:
        case "create":
            pass
        case "delete":
            pass
        case "read":
            pass
        case "write":
            pass
        case "append":
            pass
        case "rename":
            pass
        case "copy":
            pass
        case "move":
            pass
        case "ls":
            pass
        case "search":
            pass
        case _:
            raise RunningError