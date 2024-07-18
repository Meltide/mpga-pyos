import time as tm
import getpass
import datetime
import calendar
import os
import sys
import colorama
import random
from colorama import init, Fore, Back, Style
init(autoreset = True)
clsn = 0
error = 0
version = "2.0"
pkg = "8 (sys)"
tips = ["You can find the default password in the source code", "Maybe the coverter is useless :)", "'Root' is the default user.", "Is this file system real?", "Columns make the calculator work."]
while clsn != 1:
    print("Which is your host system?\n[1]Windows   [2]Other")
    print(Fore.RED + "Note: The wrong option will cause errors in PyOS.")
    cls = input("Input: ")
    if cls == "1":
        clsn = 1
    elif cls == "2":
        clsn = 1
    else:
        print("Invalid value! Please retry")
tm.sleep(0.5)
if cls == "1":
    i = os.system("cls")
elif cls == "2":
    i = os.system("clear")
for i in range(1, 101):
    print("\r", end="")
    print("Starting: {}%: ".format(i), "=" * (i // 8), end="")
    sys.stdout.flush()
    tm.sleep(0.005)
if cls == "1":
    i = os.system("cls")
elif cls == "2":
    i = os.system("clear")
print(Style.DIM + "\nPY OS (R) Core Open Source System " + version)
tm.sleep(0.1)
print(Fore.BLUE + "  __  __ ___  ___   _   \n |  \/  | _ \/ __| /_\  \n | |\/| |  _/ (_ |/ _ \ \n |_|  |_|_|  \___/_/ \_\\\n                        ")
tm.sleep(0.05)
print(Fore.YELLOW + "Make PyOS Great Again!\n")
tm.sleep(0.1)
random.shuffle(tips)
random_item = tips[0]
print("Tip: " + random_item)
tm.sleep(0.1)
print(Fore.MAGENTA + "\nAuther: AMDISYES\nAuther's QQ: 3480656548\nAuthor's Github: AMDISYES")
tm.sleep(0.1)
print(Fore.CYAN + "\nVisit this project in github: github.com/AMDISYES/pyos_core\nAlso try PyOS's improved version by minqwq and bibimingming!\n")
tm.sleep(0.25)                   
count = 0
file = "~"
stpasswd = "114514"
times = datetime.datetime.now()
while count < 3:
    user = input("Login: ")
    if user == "root":
        while count < 3:
            passwd = getpass.getpass("Password: ")
            if passwd == stpasswd:
                print("Last login: " + Fore.CYAN + times.strftime("%y/%m/%d %H:%M:%S"))
                tm.sleep(0.75)
                print("")
                while count < 3:
                    zshp9k = times.strftime(" %m/%d %H:%M:%S ")
                    if error == 1:
                        cmd = input(Back.RED + Fore.WHITE + " ✘ " + errcode + " " + Back.WHITE + Fore.BLACK + zshp9k + Back.YELLOW + " root@localhost " + Back.BLUE + Fore.WHITE + " " + file + " " + Back.RESET + "> ")
                    else:
                        cmd = input(Back.WHITE + Fore.BLACK + zshp9k + Back.YELLOW + " root@localhost " + Back.BLUE + Fore.WHITE + " " + file + " " + Back.RESET + "> ")
                    if cmd == "ls":
                        error = 0
                        if file == "~":
                            print("Downloads  Documents  Music  Pictures")
                        if file == "/":
                            print("home")
                    elif cmd == "cd" or cmd == "cd ~":
                        error = 0
                        file = "~"
                    elif cmd == "cd ..":
                        error = 0
                        file = "/"
                    elif cmd == "cd /":
                        file = "/"
                    elif cmd == "cd home":
                        file = "~"
                    elif cmd == "version":
                        error = 0
                        print("PY OS (R) Core Open Source System " + version)
                    elif cmd == "coverter":
                        error = 0
                        print("File Covert\nCovert .lpap/.lpcu/.bbc to .umm")
                        input("Input file's path:\n")
                        for i in range(1, 101):
                            print("\r", end="")
                            print("Progress: {}%: ".format(i), "=" * (i // 2), end="")
                            sys.stdout.flush()
                            tm.sleep(0.05)
                        print("\nCovert Complete.")
                    elif cmd == "time":
                        error = 0
                        other_StyleTime = times.strftime("%Y-%m-%d %H:%M:%S")
                        print(other_StyleTime)
                    elif cmd == "passwd":
                        error = 0
                        stpasswd = input("Input new password: ")
                    elif cmd == "calendar":
                        error = 0
                        today = datetime.datetime.today()
                        yy = str(today.year)#int(input("Year: "))
                        mm = str(today.month)#int(input("Month: "))
                        dd = str(today.day)
                        print(Fore.BLUE + "Now: " + yy + "-" + mm + "-" + dd)
                        c1 = 0
                        c2 = 0
                        while c1 == 0:
                            y = input("Year: ")
                            if y.isdigit() == True:
                                c1 = 1
                            else:
                                print("Invalid value! Please retype.")
                        while c2 == 0:
                            m = input("Month: ")
                            if m.isdigit() == True:
                                if int(m) > 0 and int(m) <= 12:
                                    c2 = 1
                                else:
                                    print("Invalid value! Please retype.")
                            else:
                                print("Invalid value! Please retype.")
                        print(calendar.month(int(y), int(m)))
                    elif cmd == "help":
                        error = 0
                        print("ls          View the path")
                        print("version     Show the system's version")
                        print("coverter    A tool to covert .lpap/.lpcu/.bbc to .umm")
                        print("time        Show the time and date")
                        print("calendar    Show a calendar")
                        print("calc        A simple calculator")
                        print("clear       Clean the screen")
                        print("passwd      Change your password")
                        print("neofetch    List all hardware and system version")
                        print("exit        Log out")
                        print("shutdown    Shutdown the system")
                    elif cmd == "calc":
                        error = 0
                        s1 = 0
                        while s1 == 0:
                            try:
                                formula = input("Enter the formula to be calculated (Type 'exit' to exit):\n> ")
                                if formula == "exit":
                                    s1 = 1
                                else:
                                    print("Result: " + Fore.BLUE + str(eval(formula)))
                            except Exception as e:
                                print("Input error.")
                    elif cmd == "neofetch":
                        error = 0
                        print(Fore.BLUE + "  __  __ ____   ____    _    \n |  \/  |  _ \ / ___|  / \   \n | |\/| | |_) | |  _  / _ \  \n | |  | |  __/| |_| |/ ___ \ \n |_|  |_|_|    \____/_/   \_\\\n                             ")
                        print(Fore.BLUE + "root" + Fore.RESET + "@" + Fore.BLUE + "localhost")
                        print("-----------------")
                        tm.sleep(0.05)
                        print(Fore.BLUE + "OS" + Fore.RESET + ": MPGA PyOS V2.0 aarch64")
                        if cls == "1":
                            host = "Windows CMD"
                        elif cls == "2":
                            host = "UNIX Shell"
                        tm.sleep(0.05)
                        print(Fore.BLUE + "Host" + Fore.RESET + ": " + host)
                        print(Fore.BLUE + "Kernel" + Fore.RESET + ": PTCORE-V20240716-aarch64")
                        tm.sleep(0.05)
                        print(Fore.BLUE + "Uptime" + Fore.RESET + ": 9d, 4h, 19m, 27s")
                        tm.sleep(0.05)
                        print(Fore.BLUE + "Packages" + Fore.RESET + ": " + pkg)
                        print(Fore.BLUE + "Shell" + Fore.RESET + ": pysh 1.0.0")
                        tm.sleep(0.05)
                        print(Fore.BLUE + "CPU" + Fore.RESET + ": (8) @ 2.035Ghz")
                        tm.sleep(0.05)
                        print(Fore.BLUE + "Memory" + Fore.RESET + ": " + str(random.randint(1024, 15364)) + "MiB" + "/15364MiB")
                        tm.sleep(0.05)
                        print("")
                        print(Back.BLACK + "    " + Back.RED + "    " + Back.GREEN + "    " + Back.YELLOW + "    " + Back.BLUE + "    " + Back.MAGENTA + "    " + Back.CYAN + "    " + Back.WHITE + "    ")
                        print("")
                    elif cmd == "":
                        space = 0
                    elif cmd == "clear":
                        error = 0
                        if cls == "1":
                            i = os.system("cls")
                        elif cls == "2":
                            i = os.system("clear")
                    elif cmd == "exit":
                        error = 0
                        break
                    elif cmd == "shutdown":
                        error = 0
                        count = 4
                    else:
                        print("Unknown command.")
                        error = 1
                        errcode = str(random.randint(100, 999))
            else:
                print("Error password! Please retry")
                print(Style.DIM + "Tip: You can find the default password in the source code.")
    else:
        print("Invalid user! Please retry")
        print(Style.DIM + "Tip: 'Root' is the default user.")
