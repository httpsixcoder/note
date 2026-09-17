# 整数类型
num1 = 10
num1 = 1_000_000_000
print(type(num1))  # int
print(num1)  # 1000000000

# bool True-1/False-0

num2 = True
num3 = 20
# print(type(num2)) #bool
# print(num2 + num3) #21

# print(isinstance(num2, bool))  # True
# print(isinstance(num3, bool))  # False
# print(isinstance(num2, int))  # True
# print(type(num2)==type(num3)) #False
# print("-------------------------")

# num1=0.1
# num2=0.2
# print(type(num1))
# print(type(num2))
# print(num2+num1) #0.3000004【精度丢失】
# from decimal import Decimal
# num1 = Decimal("0.1")
# num2 = Decimal("0.2")
# print(num1 + num2)

# num1=1.3e7
# print(num1)

# print(True==1)      #True
# print(False==0)     #True
# # 注意True和1值相等，但是他们不是同一个对象（不是指向内存中的同一个地址）【True对象中有Value】
# print(True is 1)    #False
# print(False is 0)   #False

# print("hello\rwor")  #wor 【在命令行中可能存在输出worlo】

# intern机制，滞留机制
# str1 = "hello world"
# str2 = "hello world"
# print(id(str1))
# print(id(str2))
# # ide中地址一致，在cmd中不一致


# num1 = 10
# num2 = 2
# num3 = num1 / num2
# # print(num3, type(num3)) #5.0 float

# print("hello" + 123) #整型和字符串相加会报错，Python无法进行隐式转换完成计算

# int(x[,base])     将x转换成整数，base指定进制
# str = "1010"
# res = int(str, 8)
# print(res)
# float(x)  将x转换成浮点数
# print(float("3.1"))
# complex(real[,imag])      创建一个实部为real，虚部为imag的复数
# str(x)    将x转换成字符串
# repr(x)   将x转换成字符串，可以转移字符串中的特殊字符
# print(repr("hello \n world"))
# eval(x)   执行x字符串表达式，病犯乎表达式的值
# eval("print(123)")
# bin((x)   整型转换成二进制字符串
# oct(x)    整型转换成八进制字符串
# hex(x)    整型转换成十六进制字符串
# ord(x)    将字符转换成ASCII整数值
# chr(x)    将整型转换为一个Unicode字符

# str1="你好中国"
# # 编码，默认字符集式utf-8
# b=str1.encode(encoding="gbk")
# print(b,type(b))
# # 解码，注意：编码使用的字符集必须和解码的字符集一致
# str2=b.decode(encoding="gbk")
# print(str2,type(str2))

name=input("请输入你的名字")
print(name)