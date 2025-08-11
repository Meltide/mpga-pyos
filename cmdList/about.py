from art import text2art
from rich import print
from rich.markup import escape

__doc__ = "Show the about of PyOS"


def print_contributors():
    contributors = {
        "MeltIce": "The author of MPGA PyOS",
        "Yukari2024": "Fix bugs",
        "MinimalMio": "Add nix running method",
        "EricDing618": "Refactor project, add functions",
        "adproqwq": "Split project, fix bugs.",
    }

    for name, value in sorted(contributors.items()):
        print(f"[blue]{name}[/]: {value}")


def execute(self, args):
    print(f"MPGA PyOS Open Source System [default not bold]{self.version}[/]")
    print('[blue]' + text2art("MPGA", font="small")+'[/]')
    print("Visit this project in github: [blue]github.com/Meltide/mpga-pyos[/]\n")
    print("[Contributors]".center(20, "="))
    print("Arranged by the first letter, in no particular order.")
    print_contributors()
    print()
    print("[Contact us]".center(20, "="))
    print(
        f"MPGA Team Telegram Group: [magenta]@MPGATeam[/]\n"
        + f"MPGA Team Matrix Group: [magenta]#MPGATeam:mozilla.org[/]"
    )
