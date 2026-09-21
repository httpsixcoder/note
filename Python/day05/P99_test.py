# 题目 1：字符串操作
# 给定字符串 my_string = “Hello, Python!”，请完成以下任务：
# 将字符串转换为大写形式。 2.查找字符串中字符 ‘P’ 的位置。 3.将字符串按照 ‘,’ 进行分割。
my_string = "Hello, Python!"
my_string = my_string.upper()
print(my_string.index("P"))
print(my_string.split(","))
# 题目 2：元组特性
# 创建一个元组 my_tuple = (1, 2, 2, 3, 4, 4, 4)，请完成：
# 计算元组中元素 4 出现的次数。 2.获取元组的长度。
my_tuple = (1, 2, 2, 3, 4, 4, 4)
print(my_tuple.count(4))
print(len(my_tuple))
# 题目 3：集合操作
# 现有集合 set1 = {1, 2, 3, 4, 5} 和 set2 = {3, 4, 5, 6, 7} 。
# 求这两个集合的并集。
# 求这两个集合的交集。
# 从 set1 中移除元素 3 。
set1 = {1, 2, 3, 4, 5}
set2 = {3, 4, 5, 6, 7}
print(set1.intersection(set2))
# 方法1：
print(set1.union(set2))
# 方法2：
print(set1 | set2)
set1.remove(3)
print(set1)
# 题目 4：集合与字典综合
# 创建一个集合，包含数字 1 到 5 。再创建一个字典，键为集合中的数字，值为该数字的平方。
set1 = {i for i in range(1,6)}
dict1 = {k: k ** 2 for k in set1}
print(set1)
print(dict1)
