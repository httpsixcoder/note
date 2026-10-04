"""
    该案例演示了类装饰器
"""
from math import sqrt

"""
class Myclass:
    def f(self):
        print('f')
    def __call__(self): #只要类实现了 __call__，它的实例就是可调用对象（Callable）。
        print('hello')

c1=Myclass()
# c1.f()
c1() #obj() 是 obj.__call__() 的语法糖。
"""
"""
# 类装饰器
def fun(x):
    return sqrt(x)
class Myclass:
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        x = abs(x)
        return self.f(x)
c1 = Myclass(fun)
print(c1(4))
"""
# 语法糖

class Myclass:
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        x = abs(x)
        return self.f(x)
@Myclass
def fun(x):
    return sqrt(x)

print(fun(-4))