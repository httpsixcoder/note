"""
    该案例演示了深拷贝和浅拷贝
"""
import copy
"""
# 浅拷贝
list1 = [1, 2, 3, [100, 200, 300]]
print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
list2 = copy.copy(list1)
print(id(list2), id(list2[0]), id(list2[1]), id(list2[2]), id(list2[3]), list2)
print("~" * 50)
# list1[0]=100
list1[3].append(400)
print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
print(id(list2), id(list2[0]), id(list2[1]), id(list2[2]), id(list2[3]), list2)
print("~" * 50)

# 深拷贝
list1 = [1, 2, 3, [100, 200, 300]]
print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
list2 = copy.deepcopy(list1)
print(id(list2), id(list2[0]), id(list2[1]), id(list2[2]), id(list2[3]), list2)
print("~" * 50)
# list1[0]=100
list1[3].append(400)
print(id(list1), id(list1[0]), id(list1[1]), id(list1[2]), id(list1[3]), list1)
print(id(list2), id(list2[0]), id(list2[1]), id(list2[2]), id(list2[3]), list2)
"""

"""
# 1.非容器类（数字，字符串，和其他“原子”类型的对象）无法拷贝
var1=1
print(id(var1),var1)
var2=copy.copy(var1)
# var2=copy.deepcopy(var1)  # 一样
print(id(var2),var2)
"""

# 2.元组变量如果只包含原子类型对象，不能对其拷贝
# 元组不光包含不可变数据类型，还包含可变数据类型，不能对其进行浅拷贝
# 元组不光包含不可变数据类型，还包含可变数据类型，能对其进行深拷贝
tuple1=(1,2,3)
print(id(tuple1),tuple1)
tuple2=copy.copy(tuple1)
print(id(tuple2),tuple2)
tuple3=copy.deepcopy(tuple1)
print(id(tuple3),tuple3)
print("~" * 50)
tuple11=(1,2,3,[10,20,30])
print(id(tuple11),tuple11)
tuple22=copy.copy(tuple11)
print(id(tuple22),tuple22)
tuple3=copy.deepcopy(tuple11)
print(id(tuple3),tuple3)


