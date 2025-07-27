from rich import print
from rich.syntax import Syntax
from pygments.lexers import get_lexer_for_filename
from ..src.pyos.utils.man import ErrorCodeManager

__doc__ = "Catch file's content"

__usage__ = {
    "[filename]": "Catch file's content"
}

def highlight_file(filepath):
    # 自动根据后缀选择高亮器
    lexer = get_lexer_for_filename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    return Syntax(code, lexer.name)

def execute(self, args):
    if not args:
        print("Error: [red]No filename provided. Please specify a valid command.[/]")
        print("Usage:")
        for command, description in __usage__.items():
            print(f"  {command}: {description}")
        raise SyntaxError
    
    print(highlight_file(args[0]))