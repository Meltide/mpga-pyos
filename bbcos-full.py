import time as tm
import getpass
import datetime
import calendar
import os
print("BBC OS (R) Core Open Source System 1.2")
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
                        print("BBC OS (R) Core Open Source System 1.2 ")
                    elif cmd == "coverter":
                        print("File Covert\nCovert .lpap/.lpcu/.bbc to .umm")
                        input("Input file's path:\n")
                        print("Coverting [____________________] 0%")
                        tm.sleep(0.3)
                        print("Coverting [######______________] 30%")
                        tm.sleep(0.3)
                        print("Coverting [############________] 60%")
                        tm.sleep(0.3)
                        print("Coverting [################____] 80%")
                        tm.sleep(0.3)
                        print("Coverting [####################] 100%")
                        tm.sleep(0.09)
                        print("Covert Complete.")
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
