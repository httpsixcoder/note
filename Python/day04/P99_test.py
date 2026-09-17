### 题目 1：分支与循环结合
# 编写一个程序，从 1 循环到 10，当数字是偶数时打印 “偶数”，奇数时打印 “奇数”。。
# str1 = ""  # 小数据使用
# res = []  # 【字符串大量拼接：优先列表 append + join】
# for i in range(1, 11):
#     # str1 += f"{i}是{'偶数' if i % 2 == 0 else '奇数'} \n"
#     res.append(f"{i}是{'偶数' if i % 2 == 0 else '奇数'} ")
# print('\n'.join(res))  # 【分隔符字符串.join(容器)】 【容器里面所有元素必须是字符串类型】
# -------------------------------------------------------------------------
# 区分 `split()` 和 `join()`（一对互操作）
# `"a,b,c".split(',')` → 按逗号切割，得到列表 `["a","b","c"]`
# `','.join(["a","b","c"])` → 列表合并为字符串 `"a,b,c"`
# -------------------------------------------------------------------------
### 题目 2：循环控制
# 使用for循环，打印如下图形的*
#     *
#    ***
#   *****
#  *******
# *********
# for i in range(1, 6):
#     print(f"{' ' * (5 - i)}{'*' * (i * 2 - 1)}")  # {表达式}
# 双层嵌套
# for i in range(1, 6):
#     for j in range(i, 5):
#         print(' ', end='')
#     for j in range(i * 2 - 1):
#         print('*', end='')
#     print()
# 格式化输出
# n = 5
# for i in range(1, n + 1):
#     print(f"{'*' * (i * 2 - 1)}".center(2*n-1))  # f"{表达式:格式}"
### 题目 3：列表操作
# 现有列表 my_list = [10, 20, 30, 40, 50]，请编写代码实现：
# list1 = [10, 20, 30, 40, 50]
# # 1. 向列表末尾添加一个元素 60。
# list1.append(60)
# print(list1)
# # 1. 取出列表中索引为 2 的元素。
# print(list1[2])
# # 1. 计算列表中所有元素的和。
# print(sum(list1))
# ------------------------------------------------------------------------------------------------
# 1）给定一个列表numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]，编写一个程序，将列表中所有的偶数元素删除
# # 遍历列表的副本，避免在迭代时修改原列表导致的问题
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# res = [i for i in numbers if i % 2 != 0]
# print(res)
# 2）创建一个空列表fruits，然后添加 "apple", "banana", "cherry", "date" 四个元素。
# 接着在列表的开始添加 "elderberry"，在 "cherry" 之前添加 "fig"，并将列表的最后一个元素替换为 "grape"。
# fruits = []
# fruits.extend(["apple", "banana", "cherry", "date"])
# fruits.insert(0, "elderberry")
# fruits.insert(fruits.index("cherry"), "fig")
# print(fruits)
# 3）给定一个列表prices = [10.5, 20.0, 15.75, 8.2, 12.0]，
# 编写一个程序，将列表中的元素都乘以 1.1（表示增加 10%），并将结果存储在一个新列表new_prices中。
# prices = [10.5, 20.0, 15.75, 8.2, 12.0]
# new_prices = [i * 1.1 for i in prices]
# new_prices1 = [f"{i * 1.1:.2f}" for i in prices]    #列表元素转换成字符串
# new_prices2 = [round(i * 1.1, 2) for i in prices]   #列表元素还是数值
# 【round 是 "银行家舍入"，四舍六入五成双，等于 5：看前一位，偶数就舍去，奇数就进1】
# print(new_prices)
# print(new_prices1)
# print(new_prices2)
# 4）有两个列表list1 = [1, 2, 3, 4, 5]和list2 = [6, 7, 8, 9, 10]，
# 将它们合并为一个新列表combined_list，并对combined_list进行降序排序
# list1 = [1, 2, 3, 4, 5]
# list2 = [6, 7, 8, 9, 10]
# combined_list = list1 + list2
# combined_list.sort(reverse=True)
# print(combined_list)
# 5）给定一个列表strings = ["hello", "world", "python", "is", "fun"]，
# 编写一个程序，将列表中的元素拼接成一个字符串，元素之间用空格分隔。
# strings = ["hello", "world", "python", "is", "fun"]
# res_str = ' '.join(strings)
# print(res_str)
# 6）给定一个字符串sentence = "Hello, World!"，编写一个程序，将字符串中的所有小写字母转换为大写字母，并输出结果。
# sentence = "Hello, World!"
# print(sentence.upper())
# # 7）给定一个字符串text = "Python is fun and powerful."，统计字符串中字母n出现的次数。
# text = "Python is fun and powerful."
# print(text.count('n'))
# # 8）给定一个字符串str1 = "apple,banana,cherry,date"，
# # 将该字符串按照,分隔，存储在一个列表中，并将列表中的元素首字母大写，最后将修改后的列表元素用-连接成一个新的字符串。
# str1 = "apple,banana,cherry,date"
# print('-'.join(str1.title().split(',')))
# 9）给定一个元组fruits = ("apple", "banana", "cherry", "date", "elderberry")，编写一个程序，找出元组中最长的元素。
#
# 10）给定两个集合set1 = {1, 2, 3, 4, 5}和set2 = {4, 5, 6, 7, 8}，编写一个程序，找出两个集合的交集、并集以及差集。
#
# 11）给定一个集合original_set = {1, 2, 3, 4, 5}，编写一个程序，向集合中添加元素 6 和 7，并从集合中移除元素 3。
#
# 12）给定一个字典student_scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 88}，编写一个程序，将每个学生的分数增加 5 分，并将结果存储在一个新的字典updated_scores中。
#
# 13）给定一个字典fruit_prices = {"apple": 1.2, "banana": 0.5, "cherry": 2.5, "date": 3.0}，编写一个程序，找出价格最高的水果及其价格。
