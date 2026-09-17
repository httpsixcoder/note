# 9）遍历出1~100之间所有的数,将能被3整除的数打印出来,每行打印5个
# let = 0
# for i in range(1, 101):
#     if i % 3 == 0:
#         print(i, end="\t")
#         let += 1
#         if let % 5 == 0: print()
# 10）计算1+2+3+...+100的和
# sumN = 0
# for i in range(1, 101):
#     sumN += i
# print(sumN)
# 11）接收用户在键盘上输入的正整数,如果输入-1结束,找出其中输入最大的值
# maxN = None #避免
# while True:
#     val = int(input("请输入数字"))
#     if val == -1: break
#     if val > maxN: maxN = val
# print(maxN)
# 12）求出2~10这些数字中的质数
# 	质数:在一个大于1的自然数中,如果只能被1和自身整除的数
# import math
# # 利用for...else
# for i in range(2, 11):
#     for j in range(2, int(math.isqrt(i)) + 1):  # 非负整数求整数平方根，无浮点误差
#         if i % j == 0: break
#     else:
#         print(i, end=" ")
# # flag标记
# for i in range(2, 11):
#     flag = True
#     for j in range(2, int(math.isqrt(i)) + 1):  # 只循环到平方根！减少一半循环
#         if i % j == 0:
#             flag = False
#             break
#     if flag:
#         print(i, end=" ")
# 13）打印如下图形的*
# 	*
# 	* *
# 	* * *
# 	* * * *
# 	* * * * *
# for i in range(5):
#     for j in range(i+1):
#         print("*",end=' ')
#     print()
# for i in range(1,6): #每项都一样，一层循环
#     print("* " * i)
