from colorama import Fore #彩色文字库
from utils.man import ErrorCodeManager

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
                self.error_code = 115
            else:
                print(f"Result: {Fore.BLUE}{str(eval(formula))}")
                self.error_code = 0
        except Exception as e:
            print(f"Error: {Fore.RED}{e}")
            self.error_code = ErrorCodeManager().get_code(e)
