'''很实用的工具箱'''

import re
import operator
from typing import List, Set, Tuple, Optional, Dict, Any, Union
from .err import PYOScriptError

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
    
    def parse_cmd(self, s):
        return CommandParser().parse_command(s)

class ExpressionEvaluator:
    def __init__(self, variables: Dict[str, Any]):
        self.variables = variables
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '^': operator.pow,
            '&': operator.and_,
            '|': operator.or_
        }
    
    def evaluate(self, expression: str, line_no: int = 0, path: str = '<module>'):
        """安全地计算表达式值"""
        try:
            # 预处理：替换变量和标准化表达式
            expr = self._preprocess_expression(expression)
            # 解析并计算表达式
            return self._evaluate_expression(expr)
        except Exception as e:
            raise PYOScriptError(f"Expression evaluation failed: {expression} -> {str(e)}",line_no,path,'Value')
    
    def _preprocess_expression(self, expr: str) -> str:
        """预处理表达式：替换变量并标准化格式"""
        # 替换变量引用
        for var_name, value in self.variables.items():
            # 只替换完整的变量名（避免替换变量名的一部分）
            expr = re.sub(rf'\b{var_name}\b', self._format_value(value), expr)
        
        # 标准化布尔值
        expr = expr.replace('True', 'true').replace('False', 'false')
        return expr
    
    def _format_value(self, value: Any) -> str:
        """将值转换为表达式中的字符串表示"""
        if isinstance(value, str):
            return f'"{value}"'  # 字符串加引号
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        return str(value)
    
    def _evaluate_expression(self, expr: str) -> Any:
        """递归计算表达式"""
        expr = expr.strip()
        
        # 处理括号
        if '(' in expr:
            return self._evaluate_parentheses(expr)
        
        # 处理运算符（按优先级顺序）
        for ops in [['^'], ['*', '/'], ['+', '-'], ['&', '|']]:
            parts = self._split_by_operators(expr, ops)
            if len(parts) > 1:
                return self._evaluate_operator_expression(parts, ops)
        
        # 基础值处理
        return self._parse_literal(expr)
    
    def _evaluate_parentheses(self, expr: str) -> Any:
        """处理带括号的表达式"""
        stack = []
        result = []
        current = []
        
        for char in expr:
            if char == '(':
                stack.append(current)
                current = []
            elif char == ')':
                if stack:
                    inner_expr = ''.join(current)
                    evaluated = str(self._evaluate_expression(inner_expr))
                    current = stack.pop() + [evaluated]
                else:
                    current.append(char)
            else:
                current.append(char)
        
        return self._evaluate_expression(''.join(current))
    
    def _split_by_operators(self, expr: str, operators: list) -> list:
        """按指定运算符分割表达式（考虑运算符优先级）"""
        pattern = '|'.join(re.escape(op) for op in operators)
        parts = re.split(f'({pattern})', expr)
        return [p.strip() for p in parts if p.strip()]
    
    def _evaluate_operator_expression(self, parts: list, operators: list) -> Any:
        """计算运算符表达式"""
        if len(parts) == 1:
            return self._evaluate_expression(parts[0])
        
        # 找到第一个运算符的位置
        op_pos = next((i for i, p in enumerate(parts) if p in operators), None)
        if op_pos is None:
            return self._evaluate_expression(parts[0])
        
        op = parts[op_pos]
        left = self._evaluate_expression(''.join(parts[:op_pos]))
        right = self._evaluate_expression(''.join(parts[op_pos+1:]))
        
        # 处理字符串拼接
        if op == '+' and (isinstance(left, str) or isinstance(right, str)):
            return str(left) + str(right)
        
        # 数值运算
        try:
            left_num = float(left) if not isinstance(left, (int, float)) else left
            right_num = float(right) if not isinstance(right, (int, float)) else right
            return self.operators[op](left_num, right_num)
        except (ValueError, TypeError):
            raise PYOScriptError(f"Unsupported operator: {left} {op} {right}",0,'<module>','Value')
    
    def _parse_literal(self, value_str: str) -> Any:
        """解析基础类型字面量"""
        # 处理字符串
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        if value_str.startswith("'") and value_str.endswith("'"):
            return value_str[1:-1]
        
        # 处理布尔值
        if value_str.lower() == 'true':
            return True
        if value_str.lower() == 'false':
            return False
        
        # 处理数字
        try:
            if '.' in value_str or 'e' in value_str.lower():
                return float(value_str)
            return int(value_str)
        except ValueError:
            raise PYOScriptError(f"Cannot parse value: {value_str}",0,'<module>','Value')

class CommandParser:
    '''与foxShell.parse_commands不同，添加了变量解析'''
    def __init__(self):
        # 快速判断的正则（仅检查基本结构）
        self.command_check_pattern = re.compile(r'^/[a-zA-Z_]\w*(?:\s|;)')
        
        # 详细解析正则
        self.full_command_pattern = re.compile(
            r'^/(?P<command>[a-zA-Z_]\w*)'  # 命令部分
            r'(?:\s+(?P<args>(?:[^;"\'\s]+|"(?:\\"|[^"])*"|\'(?:\\\'|[^\'])*\'|`[^`]+`)*))?'  # 参数部分
            r';$'  # 结束分号
        )
        
        # 参数分割正则
        self.arg_split_pattern = re.compile(
            r'([^"\'\s`]+|"[^"]*"|\'[^\']*\'|`[^`]+`)'
        )

    def is_command(self, s: str) -> bool:
        """快速判断是否为命令格式"""
        return bool(self.command_check_pattern.match(s.strip())) and s.strip().endswith(';')

    def parse_command(self, command_str: str) -> Optional[Dict[str, Union[str, List]]]:
        """详细解析命令"""
        if not self.is_command(command_str):
            return None
        
        match = self.full_command_pattern.match(command_str.strip())
        if not match:
            return None
        
        return {
            'command': match.group('command'),
            'args': self._parse_args(match.group('args')) if match.group('args') else []
        }

    def _parse_args(self, args_str: str) -> List[Union[str, Dict]]:
        """解析参数部分"""
        args = []
        for arg_match in self.arg_split_pattern.finditer(args_str.strip()):
            arg = arg_match.group(0)
            
            if arg.startswith(('"', "'")):
                args.append(arg)  # 保留引号字符串
            elif arg.startswith('`'):
                args.append({'type': 'var', 'name': arg[1:-1]})  # 反引号变量
            else:
                args.append(arg)  # 普通参数
        
        return args