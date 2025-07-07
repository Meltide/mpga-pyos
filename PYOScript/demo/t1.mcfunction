@author "JvavLargePython"; #标明作者
@name "demo"; #脚本命令名（可用作插件）
@version "1.1.4";#版本号
@description "A test."; #描述

"""
多行
注释（字符串）
"""
# 单行注释
/help script;
/yet list; #命令
@config "system_commands" true; #临时调整config.json，指运行时修改文件，运行完成后恢复
/python; #系统命令

int a = 1;float b = 2.0;string c = "hello";bool d = true; #基本变量用法，计划支持整数、浮点数、字符串、布尔值
float e = a + b*a; #基本运算
/echo a+b;
using PyCode {
    import os
    print("hi")
} #python单、多行代码运行基本用法
using PyCode {
    print(`a`+`b`)
} #python单、多行代码运行赋值用法
pytype c = {
    def main():
        return `a`
    main()
} #python单、多行代码赋值用法

reader d = ./a.py; #读取外部文件并返回给变量
/echo c; #命令运行赋值用法（命令是不确定的，会提供一个接口来运行命令）
/exec d; 