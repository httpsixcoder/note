"""
    该案例演示了匿名函数
"""
from functools import reduce


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a // b


# 计算器函数 实现两个整数的加减乘除
# a：整数1
# b：整数2
# op：运算操作（加减乘除）


# 面向函数编程思想
def calculate(a, b, op):
    return op(a, b)


print(calculate(4, 2, add))
print(calculate(4, 2, sub))


# 使用匿名函数
def calculate_lambda(a, b, op):
    return op(a, b)


print(calculate_lambda(4, 2, lambda a, b: a + b))
print(calculate_lambda(4, 2, lambda x, y: x - y))


list1=[1,2,3]

def func1(list11):
    temp=[]
    for i in list11:
        temp.append(i*2)
    return temp
def func2(list11):
    temp=[]
    for i in list11:
        temp.append("Atguigu"+str(i))
    return temp

def func3(func,list11):
    temp=[]
    for i in list11:
        temp.append(func(i))
    return temp


print(func1(list1))
print(func2(list1))
print(func3(lambda  i:i*2,list1))
# print(func3(lambda  i:"Atguigu"+str(i),list1))
# map 返回的是一个map对象【操作所有对象】
print(list(map(lambda i: i * 2, list1)))
print([ i*2 for i in list1 ])


list2=[-1,-5,-9,0,1,5,7]
# filter 返回是一个 filter对象【过滤】
print(list(filter(lambda i: i>0, list2)))
print([i for i in list2 if i>0])

# sorted 排序，可指定按照哪一个排序
list3=[{"name":"gao","age":30},{"name":"zhao","age":20},{"name":"wang","age":25}]
print(sorted(list3, key=lambda i: i["age"]))

# reduce 返回的是具体的结果值 归约聚合 迭代操作，两个操作结果和下一个进行操作
# reduce可以接受第三个参数作为“初始值”。比如 ，就变成了从 10 开始乘。
list4=[1,2,3,4,5]
print(reduce(lambda x, y: x * y, list4))
print(reduce(lambda x, y: x * y, list4, 10))