"""
    该案例演示了装饰器
"""
from math import sqrt

"""
# 装饰器的基本使用
from math import sqrt
# 普通函数 开平方
def func(x):
     return sqrt(x)
# 装饰器
def decerator(f):
    # 在外层定义可保留的变量
    # 内层函数的参数和被装饰的函数的参数保持一致
    def inner(x):
        x=abs(x)
        return f(x)
    return inner
ff=decerator(func)
print(ff(-4))
"""
"""
# 不嵌套直接写
from math import sqrt

def func(x):
     return sqrt(x)
def decerator(f,x):
    x=abs(x)
    return f(x)
print(decerator(func, -4))
"""
"""
# 这种写法无法实现分开计数
from math import sqrt
count=0
def func1(x):
    return sqrt(x)
def func2(x):
    return sqrt(x)
def decerator(f,x):
    global count
    count+=1
    x=abs(x)
    print(count)
    return f(x)
print(decerator(func1, -4))
print(decerator(func1, -4))
print(decerator(func2, -4))
print(decerator(func2, -4))
"""
"""
# 装饰器真正写法
from math import sqrt

def func1(x):
    return sqrt(x)
def func2(x):
    return sqrt(x)
def decerator(f):
    count=0
    def inner(x):
        nonlocal count
        count+=1
        x=abs(x)
        print(f.__name__,count)
        return f(x)
    return inner

d_func1=decerator(func1)
print(d_func1(4))
print(d_func1(-4))
d_func2=decerator(func2)
print(d_func2(4))
print(d_func2(-4))
"""
"""
    装饰器的语法糖
    当在被装饰函数的前面添加@函数名，在执行时候，被装饰函数作为参数传递给@后指定的函数，并执行重新赋值的 func = decerator(func)
from math import sqrt

def decerator(f):
    def inner(x):
        x=abs(x)
        return f(x)
    return inner

@decerator
def func(x):
    return sqrt(x)

print(func(-9))
"""
"""
# 多层装饰
from math import sqrt

def get_abs(f):
    def inner(x):
        x=abs(x)
        return f(x)
    return inner
def get_int(f):
    def inner(x):
        x=int(x)
        return f(x)
    return inner
# 多个装饰器的装饰过程：里函数最近的装饰器先装饰，然后外面的装饰器在进行装饰
@get_int
@get_abs
def func(x):
    return sqrt(x)
print(func("-9"))

# abs_inn=get_abs(func)
# int_inn=get_int(abs_inn)
# print(int_inn("-9"))
"""

# 带参数的装饰器
def time(n):
    def get_abs(f):
        def inner(x):
            x=abs(x)
            for i in range(n):
                x=f(x)
            return x
        return inner
    return get_abs

# @time(2) #三层，第一层传参，time。第二层：get_abs（fun），第三层：inner操作
def fun(x):
    return sqrt(x)
# print(fun(-16))

print(time(2)(fun)(-16))

