# print("hello", end=" ")
# print("world", end=" ")

# 格式化输出
# 1.默认顺序
# int1 = 10
# float1 = 3.14
# print("int1=%d, float1=%f" % (int1, float1))
# print("int1=%d, float1=%.2f" % (int1, float1))
# 2.指定顺序字符串 .format()
# int1 = 10
# float1 = 3.14
# bool1 = True
# print("int1={}, float={}, bool={}".format(int1, float1, bool1))
# # 参数下标，0，1，2...
# print("int1={0}, bool={2}, float={1}".format(int1, float1, bool1))
# 3.设置参数
# int1 = 10
# float1 = 3.14
# bool1 = True
# print("int1={a}, float1={b},bool1={c}".format(a=int1, b=float1, c=bool1))
# 4.f-字符串
# int1 = 10
# float1 = 3.14
# bool1 = True
# print(f"int={int1}, float={float1}, bool={bool1}")
# print(f"{int1=}, {float1=}, {bool1=}") #【参数名字=参数值】
# int1 = 10
# str1 = f"{int1=}"
# str2 = f"{{int1=}}" #两层{{相当于转义
# print(str1)
# print(str2)
float1 = 31415.9
str1 = "{:*^20,.2f}".format(float1)
print(str1)
str1 = "{:*<20,.2f}".format(float1)
print(str1)
str1 = "{:*>20,.2f}".format(float1)
print(str1)
# ^<> 居中位置，英文逗号是分割多位数，3位一个逗号，
# Xd表示宽度X，%百分数显示，e科学计数法
