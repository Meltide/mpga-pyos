import json, os

# 导入配置文件
with open(os.path.join("configs", "profiles.json"), "r", encoding="utf-8") as f:
    profiles: dict = json.load(f)

with open(os.path.join("configs", "system_policys.json"), "r", encoding="utf-8") as f:
    policys: dict = json.load(f)

with open(os.path.join("configs", "commands.json"), "r", encoding="utf-8") as f:
    commands: dict = json.load(f)

with open(os.path.join("configs", "fox_config.json"), "r", encoding="utf-8") as f:
    fox: dict = json.load(f)

# profiles.json
HOSTNAME: str = profiles["hostname"]
ACCOUNTS: dict = profiles["accounts"]

# system_policys.json
ALLOW_SYSTEM_COMMANDS: bool = policys["system_commands"]
SHOW_ERROR_DETAILS: bool = policys["show_error_details"]
SHOW_AD: bool = policys["show_ad"]

# commands.json
SIGNED_COMMANDS: dict = commands["commands"]
SC_SYSTEM: list = SIGNED_COMMANDS["System"]
SC_TOOLS: list = SIGNED_COMMANDS["Tools"]
SC_GAMES: list = SIGNED_COMMANDS["Games"]
SC_POWER: list = SIGNED_COMMANDS["Power"]
SC_THIRD_PARTY: list = SIGNED_COMMANDS["Third-party"]

# fox_config.json
THEME: str = fox["theme"]
SHOW_GREETING: bool = fox["show_greeting"]

# 其他
BASEPATH: str = os.getcwd().replace("\\", "/")

# 重载 FoxShell
def reload_fox():
    with open(os.path.join("configs", "fox_config.json"), "r", encoding="utf-8") as f:
        fox: dict = json.load(f)