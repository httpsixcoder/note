# 3）在程序中定义name、age变量，将你的名字和年龄赋值，
name, age = "gao", 18
print(f"我的名字是{name}，我的年龄是{age}")
# 4）将十进制数 42 转换为二进制表示
intD1 = 42
print(f"{intD1}的二进制是{bin(intD1)[2:]}")  # 字符串切割
# 5）将二进制数 110110 转换为十进制表示
intB2 = "110110"
intD2 = int(intB2, 2)
print(f"{intB2}的十进制是{intD2}")
# 6）将二进制数 1101 转换为十六进制表示
intB3 = "1101"
print(f"{intB3}的十六进制是{hex(int(intB3))[2:]}")
# 7）将十六进制数 1A3 转换为二进制表示
intH4 = "1A3"
print(f"{intH4}的二进制是{bin(int(intH4, 16))[2:]}")
# 8）有十进制数-8，请用八位二进制小数表示的它的原码、反码、补码
#   原码：10001000
#   反码：11110111
#   补码：11111000
# 9）简单的加法计算器实现
# 要求：分别让用户输入两个加数，在程序中接收用户的输入并计算结果
add1, add2 = int(input("请输入第一个数字")), int(input("请输入第二个数字"))
print(f"{add1}+{add2}={add1 + add2}")
# 10）Python常用的运算符都有哪些类型
# 算数运算符 逻辑运算符 位运算符 比较运算符 成员运算符 身份运算符
# 海马运算符
"""
# 普通写法
x = int(input())
if x>0:
    print(x)
# 海象一行写法
if (x:=int(input()))>0:
    print(x)
# > 海象运算符可以减少单独一行赋值，精简代码，减少临时变量书写，在循环读取输入的时候很常用。
# 必须加括号！`(x:=表达式)`
"""
# 1）接收控制台输入的薪水值，如果高于15000，就投递简历
if (num1 := int(input("请输入你的工资"))) >= 15000: print("已投递简历")  # 海象运算符适用于先赋值后判断
# 2）从键盘上输入3位正整数，判断是否为水仙花数。水仙花数:3位正整数等于各个位数字的立方和
numW = int(input("请输入3位正整数"))
a, b, c = numW // 100, numW % 100 // 10, numW % 10
numCheck = (numW // 100) ** 3 + (numW % 100 // 10) ** 3 + (numW % 10) ** 3
print(f"{numW}{'' if numW == a ** 3 + b ** 3 + c ** 3 else '不'}是水仙花数")  # 三元表达式
# 3）从键盘上输入一个年份，判断是否为闰年
year = int(input("请输入年份"))
print(f"{year}{'' if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0) else '不'}是闰年")
# 4）从键盘上获取输入的数字，判断奇偶性，分别输出
num14 = int(input("请输入一个数字，判断奇偶"))
print(f"{num14}是{'偶' if num14 == 0 or num14 % 2 == 0 else '奇'}数")
# 5）模拟用户登录验证，获取键盘上的输入，如果用户名admin,密码是123，提示登录成功，否则提示登录失败
userName = input("请输入用户名")
password = input("请输入密码")
print("登录成功" if userName == "admin" and password == "123" else "登录失败")
# 6）获取键盘上输入的数字，判断正数负数和0
num16 = int(input("请输入一个数字"))
if num16 == 0:
    print(f"{num16}是0")
elif num16 > 0:
    print(f"{num16}是正数")
else:
    print(f"{num16}是负数")
# 7）从键盘上获取学生成绩，判断成绩等级
score = int(input("请输入学生成绩"))
g = "E"
if score >= 90:
    g = "A"
elif score >= 80:
    g = "B"
elif score > 70:
    g = "C"
elif score >= 60:
    g = "D"
print(g)  # print内存开销大，最好一次打印
# 8）从键盘上输入一个时间，输出它的下一秒时间
h, m, s = map(int, (input(), input(), input())) #  序列解包 ,map函数：把元组里面每一个字符串，依次传入 int () 转为整数，返回迭代器
total = h * 3600 + m * 60 + s  # 化成数字，减少判断
total %= 86400
nh = total // 3600
nm = total // 60 % 60
ns = total % 60
print(f"下一秒时间：{nh}时{nm}分{ns}秒")
