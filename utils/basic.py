from colorama import Fore

class Basic:
    def __init__(self):
        self.color_modes = [Fore.WHITE, Fore.GREEN, Fore.YELLOW, Fore.RED]  # 颜色模式列表
    
    def fstring(self, message, mode=0):
        """格式化字符串
        mode: 0白色，1绿色，2黄色，3红色
        """
        return self.color_modes[mode] + message
    
    def fprint(self, message, mode=0):
        """打印消息
        mode: 0白色，1绿色，2黄色，3红色
        """
        print(self.fstring(message, mode))
    
    def clean_args(self, args):
        '''过滤和清理参数，只保留字符串类型的有效命令名'''
        clean_args = []
        for arg in args:
            if isinstance(arg, str) and arg.isidentifier():
                clean_args.append(arg)
        return clean_args