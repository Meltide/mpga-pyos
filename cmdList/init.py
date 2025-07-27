__doc__ = "init vm/home/<username> directory"
import os
from safety import rich_input
from ..src.pyos.utils.config import BASEPATH
from ..src.pyos.utils.man import PathManager


def execute(self, args):
    pm = PathManager(self)
    init_dirs = ["document", "music", "picture", "video", "download", "others"]
    init_files = {
        ".about": """# New feature

# You can do anything in /home/<username> like creating files, directories, editing files, etc.

print("Welcome to PyOS.Start your journey by typing 'help'.")
                """
    }
    user = args[0] if args else "root"
    if user == "root":
        if rich_input("[red]Do you really want to initialize the root directory? (y/n): [/]").lower() != "y":
            return
    for dir in init_dirs:
        path = os.path.join(BASEPATH, "vm/home", user, dir)
        print("Creating directory:", pm.real_to_fake(path))
        os.makedirs(path, exist_ok=True)
    for file, text in init_files.items():
        path = os.path.join(BASEPATH, "vm/home", user, file)
        print("Creating file:", pm.real_to_fake(path))
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    print("Done.")
