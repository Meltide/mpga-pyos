from colorama import Fore, Style #彩色文字库
import random #随机库

__doc__="Finger-gussing game"

def execute(self,args):
    options = ["1", "2", "3", "exit"]
    print(f"{Fore.BLUE}Finger-guess Game")
    while True:
        player_choice = input(f"Punch ({Fore.BLUE}1{Fore.RESET}:Rock/{Fore.BLUE}2{Fore.RESET}:Scissors/{Fore.BLUE}3{Fore.RESET}:Paper/{Fore.BLUE}exit{Fore.RESET}:Exiting the game)\n> ")
        computer = ""
        if player_choice not in options:
            print("Unknown choice")
            continue
        elif player_choice == "exit":
            break
        if player_choice == "1":
            player = "Rock"
        elif player_choice == "2":
            player = "Scissors"
        elif player_choice == "3":
            player = "Paper"
        computer_choice = random.choice(options)
        if computer_choice == "1":
            computer = "Rock"
        elif computer_choice == "2":
            computer = "Scissors"
        elif computer_choice == "3":
            computer = "Paper"
        print(f"Player: {Fore.CYAN}{player}")
        print(f"Computer：{Fore.CYAN}{computer}")
        if player_choice == computer_choice:
            print(f"{Fore.YELLOW}Draw！")
        elif (player_choice == "1" and computer_choice == "2") or (player_choice == "2" and computer_choice == "3") or (player_choice == "3" and computer_choice == "1"):
            print(f"{Fore.GREEN}Player win!")
        else:
            print(f"{Fore.RED}Computer win!")