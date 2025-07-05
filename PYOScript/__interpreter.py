import os
import re
from lark import Lark, Transformer, Token, Tree
from typing import Callable, Any

class PYOSTransformer(Transformer):
    def __init__(self, cmd_executor: Callable[[str, list], Any] = None):
        self.vars = {}
        self.metadata = {}
        self._execute_command = cmd_executor or self._default_cmd_executor
        self.original_config = {}

    # 元数据处理
    def author_meta(self, items):
        self.metadata["author"] = items[0].strip("\'")
    
    def name_meta(self, items):
        self.metadata["name"] = items[0].strip("\'")
    
    def version_meta(self, items):
        self.metadata["version"] = items[0].strip("\'")
    
    def desc_meta(self, items):
        self.metadata["description"] = items[0].strip("\'")
    
    def config_meta(self, items):
        config_name = items[0]
        config_value = items[1]
        
        # 存储原始值以便恢复
        if config_name not in self.original_config:
            self.original_config[config_name] = self.metadata.get(config_name, None)
        
        # 更新配置
        self.metadata[config_name] = config_value

    # 变量声明
    def int_decl(self, items):
        var_name = items[0]
        value = items[1]
        # 确保值是整数
        if not isinstance(value, int):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValueError(f"无法将 {value} 转换为整数")
        self.vars[var_name] = value
    
    def float_decl(self, items):
        var_name = items[0]
        value = items[1]
        # 确保值是浮点数
        if not isinstance(value, float):
            try:
                value = float(value)
            except (TypeError, ValueError):
                raise ValueError(f"无法将 {value} 转换为浮点数")
        self.vars[var_name] = value
    
    def string_decl(self, items):
        var_name = items[0]
        value = items[1]
        # 确保值是字符串
        if not isinstance(value, str):
            value = str(value)
        self.vars[var_name] = value
    
    def bool_decl(self, items):
        var_name = items[0]
        value = items[1]
        # 确保值是布尔值
        if isinstance(value, bool):
            self.vars[var_name] = value
        elif isinstance(value, str):
            self.vars[var_name] = value.lower() == "true"
        else:
            self.vars[var_name] = bool(value)
    
    def pytype_decl(self, items):
        var_name = items[0]
        self.vars[var_name] = items[1]

    # 表达式处理
    def binary_expr(self, items):
        left, op, right = items
        op_str = op.value if hasattr(op, 'value') else str(op)
        
        try:
            if op_str == '+':
                return left + right
            elif op_str == '-':
                return left - right
            elif op_str == '*':
                return left * right
            elif op_str == '/':
                return left / right
            else:
                raise ValueError(f"未知运算符: {op_str}")
        except TypeError as e:
            raise ValueError(f"类型错误: 无法执行 {type(left)} {op_str} {type(right)}")
    
    def paren_expr(self, items):
        return items[0]
    
    # 基本值处理
    def string_value(self, items):
        return items[0].strip('"\'')
    
    def int_value(self, items):
        return int(items[0])
    
    def float_value(self, items):
        return float(items[0])
    
    def bool_value(self, items):
        return items[0].lower() == "true"
    
    def backquote_value(self, items):
        var_name = items[0].value[1:]
        if var_name in self.vars:
            return self.vars[var_name]
        raise ValueError(f"未定义变量: {var_name}")
    
    def variable_ref(self, items):
        var_name = items[0].value
        if var_name in self.vars:
            return self.vars[var_name]
        raise ValueError(f"未定义变量: {var_name}")

    # Python代码块处理
    def py_code(self, items):
        return "".join(
            item if isinstance(item, str) 
            else item.value 
            for item in items
        )
    
    def py_block(self, items):
        code = items[0]
        try:
            # 变量替换
            for var_name, var_value in self.vars.items():
                code = code.replace(f"`{var_name}", str(var_value))
            
            # 执行Python代码
            exec(code, {"__builtins__": None}, self.vars)
            return code
        except Exception as e:
            print(f"Python执行错误: {e}")
            return None

    # 文件读取
    def reader_stmt(self, items):
        var_name = items[0]
        file_path = items[1]
        
        try:
            with open(file_path, "r") as f:
                content = f.read()
            self.vars[var_name] = content
            return content
        except Exception as e:
            print(f"文件读取错误: {e}")
            return None

    # 命令处理
    def cmd(self, items):
        cmd_name = items[0].value if isinstance(items[0], Token) else items[0].children[0].value
        args = []
        
        # 处理命令参数
        if len(items) > 1:
            # 检查items[1]是Tree还是列表
            if isinstance(items[1], Tree):
                # 如果是Tree，遍历其子节点
                for arg in items[1].children:
                    args.append(self._process_cmd_arg(arg))
            else:
                # 如果已经是列表，直接遍历
                for arg in items[1]:
                    args.append(self._process_cmd_arg(arg))
        
        try:
            return self._execute_command(cmd_name, args)
        except Exception as e:
            print(f"命令执行失败: {e}")
            raise
    
    def _process_cmd_arg(self, arg):
        """处理单个命令参数"""
        if isinstance(arg, Token):
            # 处理反引号变量
            if arg.type == "BACKQUOTE_ID":
                var_name = arg.value[1:]
                if var_name in self.vars:
                    return str(self.vars[var_name])
                raise ValueError(f"未定义变量: {var_name}")
            # 处理其他Token
            else:
                return arg.value
        # 处理已转换的值
        else:
            return str(arg)

    def _default_cmd_executor(self, cmd: str, args: list):
        """默认命令执行器"""
        print(f"[DEBUG] 执行命令: {cmd} 参数: {args}")
        
        # 特殊命令处理
        if cmd == "echo":
            print(" ".join(args))
            return True
        elif cmd == "exec":
            if args:
                try:
                    exec(args[0], {"__builtins__": None}, self.vars)
                    return True
                except Exception as e:
                    print(f"执行错误: {e}")
                    return False
        elif cmd == "python":
            # 执行Python代码
            if args:
                try:
                    exec("\n".join(args), {"__builtins__": None}, self.vars)
                    return True
                except Exception as e:
                    print(f"Python执行错误: {e}")
                    return False
        return f"{cmd}_result"

    # 注释处理
    def comment(self, _):
        return None

def create_parser(cmd_executor=None):
    grammar_path = os.path.join(os.path.dirname(__file__), "grammar.lark")
    try:
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到语法文件: {grammar_path}")

    return Lark(
        grammar,
        parser="lalr",
        transformer=PYOSTransformer(cmd_executor),
        propagate_positions=False
    )
