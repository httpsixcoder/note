# 嵌套分支
# state = 0b010
# if (state & 0b100) == 0b100: # &优先级小于==，必须加（）
#     print("大写状态")
# else:
#     if (state & 0b010) == 0b010:
#         print(f"简体中文-微软拼音-{"中文" if state & 0b001 == 0b001 else "英文"}")
#     else:
#         print("英语-美式键盘")


# 多分支 match case
# from random import randint
#
# month = randint(1, 12)
# print(f"{month}月份")
# match month:
#     case 1 | 3 | 5 | 7 | 8 | 10 | 12:
#         print("这个月有31天")
#     case 2:
#         print("这个月有28或者29天")
#     case _:
#         print("这个月有30天")

# 三目运算符
# num1, num2 = 10, 20
# print(f"{num1 if num1 > num2 else num2}")
# print(max(num1, num2))

# 循环
# while
# rabbit = 2
# week = 1
# while week <= 10:
#     print(f"第{week}周，有{rabbit}只兔子")
#     rabbit = rabbit * 2 + rabbit  #等价于 rabbit * 3
#     week += 1
#
# 打印进度条
# import time
#
# num = 1
# while num < 100:
#     print("\r" + "=" * num, end="")
#     num += 1
#     time.sleep(0.5)
# while else
# for
# 1.遍历列表
# list1 = [10, 20, 30, 40, 50]
# for i in list1:
#     print(i)
# 2.遍历字符串
# str1 = "hello world"
# for i in str1:
#     print(i)
# 3.遍历range数列
# for i in range(10): # 0-9
#     print(i)
# 循环嵌套 乘法表
# for i in range(1, 10):
#     for j in range(1, i+1):
#         print(f"{i} * {j} = {i * j}", end="\t")
#     print()
# 减少 print 调用，先拼接一行字符串再打印，IO 更快
# for i in range(1,10):
#     line = ""
#     for j in range(1,i+1):
#         line += f"{i}*{j}={i*j}\t"
#     print(line)

# 关键字
# for i in range(0, 10):
#     print(f"{'' if i % 2 == 0 else i}", end=' ')
# while True:
#     pass
# if True:
#     pass
# class A:
#     pass
# def m1():
#     pass
# --------------------------下午-------------------------------

