class Basic:
    def clean_args(self, args):
        """过滤和清理参数，只保留字符串类型的有效命令名"""
        clean_args = []
        for arg in args:
            if isinstance(arg, str) and arg.isidentifier():
                clean_args.append(arg)
        return clean_args
