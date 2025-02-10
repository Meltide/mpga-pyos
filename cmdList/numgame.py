from colorama import Fore, Style #彩色文字库
import random #随机库
__doc__ = "Number guessing game"
def numgame(self,args):
    randnum = random.randint(100, 1000)
    running = 0
    runnin = 0
    print(Fore.BLUE + "NUMBER GUESSING GAME")
    print("Numerical Range: 100-1000")
    print("Difficulty: Normal")
    print("The answer is an integer.\n")
    while running == 0:
        print("Press 'start' to start, 'exit' to exit.")
        numcmd = input("> ")
        match numcmd:
            case "start":
                print(Fore.BLUE + "GAME START")
                while runnin == 0:
                    guess = input(f"Enter the number of guesses {Style.DIM}(Press 'exit' to exit)\n{Style.RESET_ALL}> ")
                    if guess == "exit":
                        break
                    else:
                        try:
                            match int(guess):
                                case x if x < randnum:
                                    print(Fore.RED + "Less.")
                                case x if x > randnum:
                                    print(Fore.RED + "Large.")
                                case x if x == randnum:
                                    print(Fore.GREEN + "YOU WIN!")
                                    runnin = 1
                                case _:
                                    print("Unknown value.")
                        except:
                            print("Unknown value.")
            case "exit":
                break
            case "":
                space = 0
            case _:
                print("")
