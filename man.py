import importlib,json,os,subprocess

class CommandManager:
    def __init__(self,core,cmd=""):
        self.cmd = cmd
        self.core = core
        with open("config.json","r") as f:
            self.cfg=json.load(f)
            self.allcmds=self.cfg["commands"]
        self.thirds=self.allcmds["Third-party"]
        self.cmds=[cmd for category in self.allcmds.values() for cmd in category]
    def reg(self,cmd):
        self.cmd=cmd
    def pkg_name(self):
        return "cmdList.third_party."+self.cmd if self.cmd in self.thirds else "cmdList."+self.cmd
    def hasattr(self,attr):
        return hasattr(self.getpkg(),attr)
    def loaded_cmd(self):
        return self.cmd in self.cmds
    def getpkg(self):
        return importlib.import_module(self.pkg_name())
    def execute(self,args=()):
        '''支持带参数的命令'''
        if self.loaded_cmd():
            __import__(self.pkg_name(),fromlist=["execute"]).execute(*args)
        elif self.core.runsys:
            subprocess.run([self.cmd]+list(args[1]))
        else:
            raise ImportError

class PathManager:
    def __init__(self,core):
        self.core=core
        self.path=os.getcwd()