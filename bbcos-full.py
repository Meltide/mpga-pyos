import time as tm
import getpass
import datetime
import calendar
import os
import sys
print("BBC OS (R) Core Open Source System 1.2.1")
print("Avaliable update! Visit bbc.com to update")
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
                        print("BBC OS (R) Core Open Source System 1.2.1 ")
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
                        yy = int(input("Year: "))
                        mm = int(input("Month: "))
                        print(calendar.month(yy, mm))
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
                        try:
                            formula = input("Enter the formula to be calculated:\n")
                            print(formula + "=", eval(formula))
                        except Exception as e:
                            print("Input error.")
                    elif cmd == "":
                        space = "0"
                    elif cmd == "clear":
                        i = os.system("cls")
                    elif cmd == "exit":
                        break
                    else:
                        print("Unknown command.")
            else:
                print("Error password! Please retry")
    else:
        print("Invalid user! Please retry")
