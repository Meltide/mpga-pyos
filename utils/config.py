import json,os

with open("config.json", "r",encoding='utf-8') as f:
    cfg:dict = json.load(f)

HOSTNAME:str = cfg["hostname"]
ACCOUNTS:dict = cfg["accounts"]

ALLOW_SYSTEM_COMMANDS:bool = cfg["os.system"]
SHOW_ERROR_DETAILS:bool = cfg["error.details"]
SIGNED_COMMANDS:dict = cfg["commands"]

SC_SYSTEM:list=SIGNED_COMMANDS["System"]
SC_TOOLS:list=SIGNED_COMMANDS["Tools"]
SC_GAMES:list=SIGNED_COMMANDS["Games"]
SC_POWER:list=SIGNED_COMMANDS["Power"]
SC_THIRD_PARTY:list=SIGNED_COMMANDS["Third-party"]

BASEPATH:str = os.getcwd().replace("\\", "/")