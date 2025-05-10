from art import text2art
from colorama import Fore

__doc__ = "Show the about of PyOS"

def print_contributors():
    contributors = {
        "MeltIce": "The author of MPGA PyOS",
        "Yukari2024": "Fix bugs",
        "EricDing618": "Refactor project, add functions",
        "adproqwq": "Split project, fix bugs."
    }
    
    for name, value in contributors.items():
        print(f"{Fore.BLUE}{name}{Fore.RESET}: {value}")

def execute(self,args):
    print(f"MPGA PyOS Open Source System {self.version}")
    print(Fore.BLUE + text2art("MPGA", font="small"))
    print(f"Visit this project in github: {Fore.BLUE}github.com/Meltide/mpga-pyos\n")
    print("[Contributors]".center(20, "="))
    print_contributors()
    print()
    print("[Contact us]".center(20, "="))
    print(
        f"MPGA Team Telegram Group: {Fore.MAGENTA}@MPGATeam\n"
        + f"{Fore.RESET}MPGA Team Matrix Group: {Fore.MAGENTA}#MPGATeam:mozilla.org"
    )
