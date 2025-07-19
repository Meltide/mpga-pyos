from rich import print  # 彩色文字库

__doc__ = "Converts characters to ASCII"


def execute(self, args):
    ascount = 0
    while ascount == 0:
        print("[blue]ASCII Dic[/]")
        print("Choose the mode\n(1) Chr to ASCII\n(2) ASCII to Chr")
        print("Press 'exit' to exit.")
        asciic = input("> ")
        if asciic == "1":
            while ascount == 0:
                print("Enter the character you want to convert to ASCII")
                print("Press 'exit' to exit.")
                ascii = input("> ")
                if ascii == "exit":
                    break
                elif ascii == "":
                    space = 0
                else:
                    try:
                        print("Result: [blue]" + str(ord(ascii))+'[/]')
                    except:
                        print("[red]Only a single character is supported.[/]")
        elif asciic == "2":
            while ascount == 0:
                print("Enter the ASCII code you want to convert to character")
                print("Press 'exit' to exit.")
                aschx = input("> ")
                if aschx == "exit":
                    break
                elif aschx == "":
                    space = 0
                else:
                    try:
                        print("Result: [blue]" + chr(int(aschx))+'[/]')
                    except:
                        print("[red]Invalid value.[/]")
        elif asciic == "exit":
            break
        elif asciic == "":
            space = 0
        else:
            print("[red]Unknown command.[/]")
