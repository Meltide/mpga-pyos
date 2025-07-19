from rich.text import Text
from rich.console import Console

def input(prompt):
    '''禁用rich的输入，返回纯文本'''
    return Text.from_markup(input(prompt), markup=False)

def rich_input(prompt: str, prompt_style="", input_style="", markup=False, **kwargs) -> str:
    '''prompt_style: 输入提示的样式
    input_style: 输入内容的样式
    markup: 是否启用富文本输入（只针对用户输入）
    **kwargs: 其他参数，例如password=True等'''
    console = Console()
    # 渲染彩色提示
    console.print(Text(prompt, style=prompt_style), end="")
    # 捕获输入并应用样式
    user_input = console.input(Text("", style=input_style) ,markup=markup, **kwargs)
    return user_input