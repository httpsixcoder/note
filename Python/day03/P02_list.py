# list
# 创建列表对象
list1 = [100, 200, 300, 400, 500]
list2 = [10, 20, 30, 40, 50]
# 通过索引获取类表中的元素
# print(list1[0])
# 切片
# print(list1[:])
# print(list1[2:-1])
# print(list1[::-1])
# 添加
# list1.append(600)
# 相加：
# print(list1+list2)
# 乘法：
# print(list1*2)
# 修改： 【可变性】
# list1[0]=0
# list1[2:4]=["30","40","50"]
# 检查成员是否存在：
# print(100 in list1)
# print(1 in list1)
# 获取列表长度：
# print(len(list1))
# 求列表最大致，最小值，求和：
# print(max(list1))
# print(min(list1))
# print(sum(list1))
# 遍历：
# 直接遍历：   for
# for item in list1:
#     print(item)
# 下标遍历：   len(list1)
# for index in range(len(list1)):
#     print(list1[index])
# 使用enumerate：获取下标和元素
# for i, v in enumerate(list1):
#     print(i, v)
# 删除：
# del list1[2]    删除指定元素
# del list1       删除整个列表
# 嵌套：
# list3=[[1,2,3],['a','b','c'],[7,8,9]]
# 列表推导式
# list4 = []
# for i in range(4):
#     list4.append(i ** 2)
# print(list4)
# print(list5)
# 可简写为 list5 = [i ** 2 for i in range(4)]
# 带条件的squares = [i ** 2 for i in range(10) if i % 2 == 0]
# squares = []
# for i in list1:
#     for j in list2:
#         squares.append(f"{i}-->{j}")
# 简化：squares=[f"{i}-->{j}" for i in list1 for j in list2]
# zip()函数 元组
# zipped=zip(list1, list2)
# print(zipped)           #<zip object at 0x000002335660AE40> 【得到的是一个元组】
# print(list(zipped))     #[(100, 10), (200, 20), (300, 30), (400, 40), (500, 50)]
# list=[1,2,3,1,6,1] 删除所有1
# list3 = [1, 2, 3, 1, 6, 1]
# for i in range(list3.count(1)):
#     list3.remove(1)
# print(list3)
# AC1：【生成新表】
# list4=[i for i in list3 if i!=1]
# print(list4)
# AC2：【原表修改】倒序遍历索引
# for index in range(len(list3) - 1, -1, -1):
#     if list3[index] == 1:
#         del list3[index]
# print(list3)
