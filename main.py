import os
import time
from colorama import init, Fore, Back, Style
init(autoreset = True)
count = 0
print(Fore.BLUE + "Choose your system")
print("(1) MPGA PyOS V2.2")
print("(2) BBC OS V1.1")
print(Style.DIM + "Tip: BBC OS is the first version of PyOS that have an archive.")
while count == 0:
    res = input("> ")
    if res == "1":
        os.system("python pyos.py")
        break
    elif res == "2":
        os.system("python bbcos-full.py")
        break
    elif res == "":
        space = 0
    else:
        print(Fore.RED + "Invalid value.")