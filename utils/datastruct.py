'''很实用的工具箱'''

import re
import ast, operator
from typing import List, Set, Tuple, Optional, Dict, Any, Union
from .err import PYOScriptError
from collections import deque
from enum import Enum

class TokenType(Enum):
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    NAME = 'NAME'


class Token:
    def __init__(self, type_: str, value: str, line_no: int, path: str):
        self.type_ = type_
        self.value = value
        self.line_no = line_no
        self.path = path
    
    def __str__(self):
        return f"{self.type_}: {self.value} (line {self.line_no}, {self.path})"
    
class Lexer:
    def __init__(self, text: str, line_no: int = 1, path: str = '<module>', vars: Dict[str, Any] = {}, var_types: Dict[str, type] = {}):
        self.text = text
        self.stripped = text.strip()
        self.line_no = line_no
        self.ds = DataStruct()
        self.vars = vars
        self.var_types = var_types
        self.ds = DataStruct()
        self.path = path
        self.mode = ''

    def tokenize(self) -> List[Token]:
        """
        词法分析器，将文本分割为Token列表
        """
        tokens = []
        for code in self.ds.strict_split(self.stripped, ';'):
            for t in self.ds.strict_split(code, ' '):
                if t.strip():
                    if String(t).is_invalid():...

class String:
    def __init__(self, value: str):
        self.value = value
    def is_invalid(self):
        return not (
            self.value.startswith('"') and self.value.endswith('"') or
            self.value.startswith("'") and self.value.endswith("'")
        )
    def get_v(self):
        return self.value[1:-1]
                
class DataStruct:
    def strict_split(
        self,
        text: str,
        delimiter: str,
        enclosing_chars: Optional[Set[Tuple[str, str]]] = None,
        keep_delimiters: bool = False,
        escape_chars: Set[str] = {'\\'},
        double_escape: bool = False
    ) -> List[str]:
        """
        增强版严格分隔函数，支持复杂转义场景
        
        参数:
            text: 要分割的文本
            delimiter: 分隔字符
            enclosing_chars: 需要忽略分隔符的字符组，默认为引号 {('"', '"'), ("'", "'")}
            keep_delimiters: 是否在结果中保留分隔符
            escape_chars: 转义字符集合，默认为 {'\\'}
            double_escape: 是否支持双转义（如 \\\\表示字面量反斜杠）
            
        返回:
            分割后的文本列表
        """
        # 默认设置
        enclosing_pairs = enclosing_chars or {('"', '"'), ("'", "'")}
        escape_chars = escape_chars or {'\\'}
        
        # 构建字符映射
        open_to_close = {op: cl for op, cl in enclosing_pairs}
        close_to_open = {cl: op for op, cl in enclosing_pairs}
        
        # 状态变量
        stack = []       # 跟踪开启的字符组
        escape_mode = 0  # 0=未转义, 1=单转义, 2=双转义
        current = []     # 当前段落的字符
        results = []     # 结果列表
        
        for char in text:
            if escape_mode > 0:
                # 处理转义状态
                current.append(char)
                if double_escape and escape_mode == 1 and char in escape_chars:
                    escape_mode = 2  # 进入双转义
                else:
                    escape_mode = 0  # 重置转义状态
            elif char in escape_chars:
                # 开始转义
                current.append(char)
                escape_mode = 1
            elif stack and char == stack[-1]:
                # 关闭当前字符组（只有非转义状态才有效）
                current.append(char)
                stack.pop()
            elif char in close_to_open:
                # 无效的关闭字符（不匹配的关闭）
                current.append(char)
            elif char in open_to_close:
                # 开启新的字符组
                current.append(char)
                stack.append(open_to_close[char])
            elif not stack and char == delimiter:
                # 只有在最外层且非转义状态才分割
                results.append(''.join(current))
                current = []
                if keep_delimiters:
                    current.append(char)
            else:
                # 普通字符
                current.append(char)
        
        # 添加最后一部分
        if current:
            results.append(''.join(current))
        
        # 返回非空结果
        return [s.strip() for s in results if s.strip()]

    def strict_replace(self, text:str, old=' ', new='') -> List[str]:
        """
        替换text中的在字符串外的old字符为new字符
        """
        return new.join(self.strict_split(text, old))
    
    def expression_evaluator(self, variables: Dict[str, Any], expression: str, line_no: int = 0, path: str = '<module>'):
        ee = ExpressionEvaluator(variables)
        return ee.evaluate(expression, line_no, path)
    
    def parse_cmd(self, s, variables: Dict[str, Any], line_no: int = 0, path: str = '<module>'):
        return CommandParser(variables,path).parse_command(s)

class ExpressionEvaluator:
    def __init__(self, variables: Dict[str, Any]):
        self.variables = variables
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitAnd: operator.and_,
            ast.BitOr: operator.or_,
            ast.USub: operator.neg,
            ast.Not: operator.not_
        }
        self.comparison_operators = {
            ast.Eq: operator.eq,
            ast.NotEq: operator.ne,
            ast.Lt: operator.lt,
            ast.LtE: operator.le,
            ast.Gt: operator.gt,
            ast.GtE: operator.ge,
            ast.Is: lambda a, b: a is b,
            ast.IsNot: lambda a, b: a is not b,
            ast.In: lambda a, b: a in b,
            ast.NotIn: lambda a, b: a not in b
        }
    
    def evaluate(self, expression: str, line_no: int = 0, path: str = '<module>'):
        """安全地计算表达式值"""
        try:
            # 预处理表达式，替换变量引用
            expr = self._preprocess_expression(expression)
            # 解析并计算表达式
            return self._evaluate_ast(expr)
        except Exception as e:
            raise PYOScriptError(f"Expression evaluation failed: {expression} -> {str(e)}", line_no, path, 'Value')
    
    def _preprocess_expression(self, expr: str) -> str:
        """预处理表达式：替换变量引用为它们的值"""
        # 标准化布尔值和None
        expr = expr.replace('True', 'true').replace('False', 'false').replace('None', 'null')
        
        # 使用正则匹配所有可能的变量名
        var_pattern = re.compile(r'\b([a-zA-Z_]\w*)\b')
        
        def replace_var(match):
            var_name = match.group(1)
            if var_name in {'true', 'false', 'null'}:  # 已经标准化的值
                return var_name
            if var_name in self.variables:
                value = self.variables[var_name]
                return self._format_value(value)
            return match.group(0)  # 不是变量则保持不变
        
        return var_pattern.sub(replace_var, expr)
    
    def _format_value(self, value: Any) -> str:
        """将值转换为可在表达式中使用的字符串表示"""
        if isinstance(value, str):
            return f'"{value}"'  # 字符串加引号
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif value is None:
            return 'null'
        return str(value)
    
    def _evaluate_ast(self, expr: str) -> Any:
        """使用AST安全地评估表达式"""
        try:
            node = ast.parse(expr, mode='eval')
            return self._eval_node(node.body)
        except (SyntaxError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid expression: {expr}") from e
    
    def _eval_node(self, node):
        """递归评估AST节点"""
        if isinstance(node, ast.Num):  # 数字
            return node.n
        elif isinstance(node, ast.Str):  # 字符串
            return node.s
        elif isinstance(node, ast.Name):  # 名称 (true/false/null)
            if node.id == 'true':
                return True
            elif node.id == 'false':
                return False
            elif node.id == 'null':
                return None
            raise ValueError(f"Unexpected identifier: {node.id}")
        elif isinstance(node, ast.BinOp):  # 二元运算
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.operators:
                return self.operators[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):  # 一元运算
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.operators:
                return self.operators[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Compare):  # 比较运算
            left = self._eval_node(node.left)
            results = []
            for op, right_node in zip(node.ops, node.comparators):
                right = self._eval_node(right_node)
                op_type = type(op)
                if op_type in self.comparison_operators:
                    results.append(self.comparison_operators[op_type](left, right))
                else:
                    raise ValueError(f"Unsupported comparison operator: {op_type.__name__}")
                left = right
            return all(results)
        elif isinstance(node, ast.BoolOp):  # 布尔运算 (and/or)
            values = [self._eval_node(v) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            elif isinstance(node.op, ast.Or):
                return any(values)
            else:
                raise ValueError("Unsupported boolean operator")
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")

class CommandParser:
    def __init__(self, variables: Dict[str, Any], path: str = '<module>'):
        self.vars = variables
        self.path = path
        # 预编译命令解析正则表达式
        self.CMD_REGEX = re.compile(r'''
            ^/
            (?P<command>[a-zA-Z_]\w*)
            (?:
                \s+
                (?P<args>
                    (?:
                        [^;\s"']+
                        |
                        "(?:\\.|[^"\\])*"
                        |
                        '(?:\\.|[^'\\])*'
                    )+
                )
            )?
            ;$
        ''', re.VERBOSE)
        
        # 预编译参数分割正则表达式
        self.ARG_REGEX = re.compile(r'''
            ([^"\'\s]+)      # 未引用的参数(可能包含变量)
            |
            "((?:\\.|[^"\\])*)"  # 双引号字符串
            |
            '((?:\\.|[^'\\])*)'  # 单引号字符串
        ''', re.VERBOSE)
        
        # 构建变量名正则模式(按长度降序确保最长匹配)
        self.VAR_REGEX = re.compile(
            r'(?<!\w)(' + '|'.join(
                sorted(
                    (re.escape(k) for k in self.vars.keys()),
                    key=len,
                    reverse=True
                )
            ) + r')(?!\w)'
        )

    def parse_command(self, command_str: str):
        """解析命令字符串，自动识别变量(不需要反引号)"""
        match = self.CMD_REGEX.fullmatch(command_str)
        if not match:
            return None
        
        result = {
            'command': match.group('command'),
            'args': []
        }
        
        if match.group('args'):
            for arg_match in self.ARG_REGEX.finditer(match.group('args')):
                # 处理未引用的参数(可能包含变量)
                if arg_match.group(1):
                    arg = arg_match.group(1)
                    # 替换变量引用
                    arg = self._replace_variables(arg)
                    result['args'].append(arg)
                
                # 处理双引号字符串(保留引号，不替换变量)
                elif arg_match.group(2):
                    result['args'].append(f'"{arg_match.group(2)}"')
                
                # 处理单引号字符串(保留引号，不替换变量)
                elif arg_match.group(3):
                    result['args'].append(f"'{arg_match.group(3)}'")
        
        return result

    def _replace_variables(self, arg: str) -> Any:
        """替换参数中的变量引用"""
        # 检查整个参数是否是单个变量
        if arg in self.vars:
            return self.vars[arg]
        
        # 检查参数中是否包含变量
        def replace_match(match):
            var_name = match.group(1)
            return str(self.vars.get(var_name, match.group(0)))
        
        # 替换参数中的变量引用
        return self.VAR_REGEX.sub(replace_match, arg)