# 每日一考
# 编写一个程序，从 1 循环到 10，当数字是偶数时打印 “偶数”，奇数时打印 “奇数”。
# for i in range(1, 11):
#     print(f"{i}是{"偶数" if i % 2 == 0 else "奇数"}")
# 使用for循环，打印如下图形的*
# ```python
#     *
#    ***
#   *****
#  *******
# *********
# # 定义等腰三角形的行数
# n = 5
# ```
# n = 5
# for i in range(1, n + 1):
#     print(" " * (5 - i),end="")
#     print("*" * (2*i-1))
# 现有列表 my_list = [10, 20, 30, 40, 50]，请编写代码实现：
# my_list = [10, 20, 30, 40, 50]
# # 1. 向列表末尾添加一个元素 60。
# my_list.append(60)
# print(my_list)
# # 1. 取出列表中索引为 2 的元素。
# print(my_list[2])
# # 1. 计算列表中所有元素的和。
# print(sum(my_list))
# -----------------------------------------------------------------------------------
# str1 = "asdjklasdaa"
# print(str1.replace('a', 'z'))
# print(str1.replace('a', 'z', 1))
# str2 = "my,name,is,gao"
# str22 = str2.split(',')
# print(str22, type(str22))
# str22 = str2.split(',',2)
# print(str22, type(str22))
# str22 = str2.rsplit(',',2)
# print(str22, type(str22))
# list1 = ["10", "20", "30"]
# print('-'.join(list1))
# str3="   hello   "
# print(str3.strip())
# str3="xxxhelloxxx"
# print(str3.strip('x'))
# str3="xxxhelloxxx"
# print(str3.removeprefix('x'))
# str3="xxxhelloxxx"
# print(str3.removesuffix('x'))
# str4="abcd ABCD aAbB AaBa"
# print(str4.upper())
# print(str4.lower())
# print(str4.swapcase())
# print(str4.capitalize())
# print(str4.title())
# print(str4.casefold())
# str5 = "abcdz"
# print(len(str5))
# print(max(str5))
# print(min(str5))
# str6="abcba"
# print(str6.find('b'))
# print(str6.rfind('b'))
# print(str6.find('z')) #-1
# print(str6.index('b'))
# print(str6.rindex('b'))
# print(str6.index('z')) #报错
# print(str6.count('b'))
# str7="abc"
# print(str7.startswith("a"))
# print(str7.endswith("c"))
# str8=" "
# print(str8.isspace())
# ------------------------------------------------------
# tup1=(100,200,300)
# print(tup1)
# tup2=(100,)
# print(tup2)
# tup_gen=(i*2 for i in range(10))
# tup3=tuple(tup_gen)
# tup4=tuple((i*2 for i in range(10)))
# print(tup3,type(tup3))
# print(tup4,type(tup4))
# tup5=(100,200,300)
# for item in tup5:
#     print(item)
# for i in range(len(tup5)):
#     print(i,tup5[i])
# for item,index in enumerate(tup5):
#     print(item,index)
# ------------------------------------------------------
# set1={100,200,300,400,500}
# set2=set([100,200])
# set3=set() #创建空的集合
# dict1={} #创建字典
