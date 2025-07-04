from interpreter import create_parser,os

def my_cmd_executor(cmd: str, args: list):
    print(f"执行命令: {cmd}, 参数: {args}")
    return True

def test():
    parser = create_parser(cmd_executor=my_cmd_executor)
    
    # 测试脚本
    script_path = os.path.join(os.path.dirname(__file__), "demo","t1.mcfunction")
    with open(script_path, "r", encoding="utf-8") as f:
        script = f.read()
    
    result = parser.parse(script)
    print("执行成功！")
    print("变量状态:", parser.parser.transformer.vars)


if __name__ == "__main__":
    test()