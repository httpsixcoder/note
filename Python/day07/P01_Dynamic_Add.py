"""
    该案例演示了动态添加属性及其方法
"""
import types

"""
# 动态的给实例添加属性
class Person:
    def __init__(self, name):
        self.name = name

    def m1(self):
        self.address = "北京"

p=Person("Zs")
# print(p.name)
# p.age=20
# print(p.age)
p.m1()
print(p.address)
"""
"""
# 动态的给类添加属性
class Person:
    def __init__(self, name):
        self.name = name
Person.home="earch"

print(Person.home)
zs=Person("Zs")
ls=Person("ls")
print(zs.home)
print(ls.home)
"""
"""
# 动态给实例添加方法
class Person:
    def __init__(self, name=None):
        self.name = name

def eat():
    print("eating")

zs=Person("Zs")
zs.eat=eat
zs.eat()
"""
"""
# 动态给实例添加实例方法
class Person:
    def __init__(self, name):
        self.name = name
def eat(self):
    print("eating")
zs=Person("Zs")
zs.bb=types.MethodType(eat,zs)
zs.bb()
"""

"""
# 动态给类添加方法
class Person:
    home = "earch"

    def __init__(self, name):
        self.name = name


# 定义类方法
@classmethod
def eat(cls):
    print(f"{cls.home} eating")


# 定义静态方法
@staticmethod
def say():
    print("say say say")


Person.eat = eat
Person.eat()
Person.say = say
Person.say()
"""
"""
# 在类外定义的函数
def func1(self,x,y):
    print(x&y)
class C:
    f=func1

# C() 创建了一个 C 的实例
C().f(6,13)
"""
# ---------------------------------------------------------------
"""
# 动态删除属性与方法
class Person:
    def __init__(self, name):
        self.name = name
    def eat(self):
        print("eating")
zs=Person("Zs")
# print(zs.name)
# del  zs.name
# print(zs.name)
zs.eat()
del zs.eat
zs.eat()
"""
# ---------------------------------------------------------------


# 限制添加实例属性与实例方法

class Person:
    __slots__ = ("name", "age","eat")
    def __init__(self, name):
        self.name = name

def eat(self):
    print(f"{self.name}eating")
def drink(self):
    print(f"{self.name}drinking")

p=Person("Zs")
# 添加实例属性
p.age=10
print(p.age)
# 添加实例方法
p.eat=types.MethodType(eat,p)
p.eat()

# 限制属性和方法
# __slots__ = ("name", "age","eat")
# p.weight=10
# print(p.weight)
# p.drink=types.MethodType(drink.p)
# p.drink()














