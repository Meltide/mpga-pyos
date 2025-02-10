from colorama import Fore #彩色文字库

__doc__="A simple calculator"

def execute(self,args):
    s1 = 0
    while s1 == 0:
        try:
            formula = input("Enter the formula to be calculated (Type 'exit' to exit):\n> ")
            if formula == "exit":
                s1 = 1
            elif not all(char in '0123456789+-*/' for char in formula): #防止恶意运行Python其他代码
                print(f"{Fore.RED}Input error.")
            else:
                print(f"Result: {Fore.BLUE}{str(eval(formula))}")
        except Exception as e:
            print(f"{Fore.RED}Input error.")
