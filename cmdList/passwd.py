import json #解析和保存json配置文件
import base64 #加解密库
__doc__="Change your password"
def execute(self,args):
    npassword = input("Input new password: ")
    with open("pwd", "r+") as pswd:
        bs64 = str(base64.b64encode(npassword.encode("utf-8")))
        pswd.truncate()
        pswd.write(bs64.strip("b'"))
    print("The password takes effect after the restart.")

