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
version = "2.0"
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
tm.sleep(0.2)
print(Fore.BLUE + "  __  __ ___  ___   _   \n |  \/  | _ \/ __| /_\  \n | |\/| |  _/ (_ |/ _ \ \n |_|  |_|_|  \___/_/ \_\\\n                        ")
tm.sleep(0.1)
print(Fore.YELLOW + "Make PyOS Great Again!\n")
tm.sleep(0.15)
random.shuffle(tips)
random_item = tips[0]
print("Tip: " + random_item)
tm.sleep(0.15)
print(Fore.MAGENTA + "\nAuther: AMDISYES\nAuther's QQ: 3480656548\nAuthor's Github: AMDISYES")
tm.sleep(0.15)
print(Fore.CYAN + "\nVisit this project in github: github.com/AMDISYES/pyos_core\nAlso try PyOS's improved version by minqwq and bibimingming!\n")
tm.sleep(0.5)                   
count = 0
stpasswd = "114514"
while count < 3:
    user = input("Login: ")
    if user == "root":
        while count < 3:
            passwd = getpass.getpass("Password: ")
            if passwd == stpasswd:
                tm.sleep(1.5)
                while count < 3:
                    cmd = input("~ $ ")
                    if cmd == "ls":
                        print("Downloads  Documents  Music  Pictures")
                    elif cmd == "version":
                        print("PY OS (R) Core Open Source System " + version)
                    elif cmd == "coverter":
                        print("File Covert\nCovert .lpap/.lpcu/.bbc to .umm")
                        input("Input file's path:\n")
                        for i in range(1, 101):
                            print("\r", end="")
                            print("Progress: {}%: ".format(i), "=" * (i // 2), end="")
                            sys.stdout.flush()
                            tm.sleep(0.05)
                        print("\nCovert Complete.")
                    elif cmd == "time":
                        now = datetime.datetime.now()
                        other_StyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
                        print(other_StyleTime)
                    elif cmd == "passwd":
                        stpasswd = input("Input new password: ")
                    elif cmd == "calendar":
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
                        print("ls          View the path")
                        print("version     Show the system's version")
                        print("coverter    A tool to covert .lpap/.lpcu/.bbc to .umm")
                        print("time        Show the time and date")
                        print("calendar    Show a calendar")
                        print("calc        A simple calculator")
                        print("clear       Clean the screen")
                        print("passwd      Change your password")
                        print("exit        Log out")
                    elif cmd == "calc":
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
                    elif cmd == "":
                        space = "0"
                    elif cmd == "clear":
                        if cls == "1":
                            i = os.system("cls")
                        elif cls == "2":
                            i = os.system("clear")
                    elif cmd == "exit":
                        break
                    else:
                        print("Unknown command.")
            else:
                print("Error password! Please retry")
                print(Style.DIM + "Tip: You can find the default password in the source code.")
    else:
        print("Invalid user! Please retry")
        print(Style.DIM + "Tip: 'Root' is the default user.")
