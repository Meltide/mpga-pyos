from colorama import Fore, Style #彩色文字库

__doc__ = "Converts characters to ASCII"

def execute(self,args):
    ascount = 0
    while ascount == 0:
        print(Fore.BLUE + "ASCII Dic")
        print(
            "Choose the mode\n(1) Chr to ASCII\n(2) ASCII to Chr"
        )
        print(Style.DIM + "Press 'exit' to exit.")
        asciic = input("> ")
        if asciic == "1":
            while ascount == 0:
                print(
                    "Enter the character you want to convert to ASCII"
                )
                print(
                    Style.DIM + "Press 'exit' to exit."
                )
                ascii = input("> ")
                if ascii == "exit":
                    break
                elif ascii == "":
                    space = 0
                else:
                    try:
                        print(
                            "Result: "
                            + Fore.BLUE
                            + str(ord(ascii))
                        )
                    except:
                        print(
                            Fore.RED
                            + "Only a single character is supported."
                        )
        elif asciic == "2":
            while ascount == 0:
                print(
                    "Enter the ASCII code you want to convert to character"
                )
                print(
                    Style.DIM + "Press 'exit' to exit."
                )
                aschx = input("> ")
                if aschx == "exit":
                    continue
                elif aschx == "":
                    space = 0
                else:
                    try:
                        print("Result: "+ Fore.BLUE+ chr(int(aschx)))
                    except:
                        print(Fore.RED + "Invalid value.")
        elif asciic == "exit":
            break
        elif asciic == "":
            space = 0
        else:
            print(Fore.RED + "Unknown command.")
