__doc__ = "Parameter return"

def execute(self, args):
    for message in args:
        print(message, end=" ")
    print("\b")