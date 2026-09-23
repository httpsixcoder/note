"""
    该案例演示了封装，成员私有化
"""
"""
# 成员名 以单下划线开始，只是一个标记，不具备强制性
class Girl:
    def __init__(self,name,age):
        self.name=name
        self._age=age
    def guangjie(self):
        print("guangjie")

ls=Girl("ls",18)
print(ls.name)
print(ls._age)
"""
"""
# 成员名 以双下划线开始，至多一个下划线结束，在类外不能被访问,在类中可以被访问
class Girl:
    def __init__(self,name,age):
        self.name=name
        self.__age=age
    def __guangjie(self):
        print(f"{self.__age}的{self.name}guangjie")

ls=Girl("ls",18)
print(ls.name)
# print(ls.__age) # 报错
# ls.__guangjie()# 报错
"""
"""
# 私有化的实现原理：底层是通过改名实现私有化  _类名__名
class Girl:
    def __init__(self,name,age):
        self.name=name
        self.__age=age
    def __guangjie(self):
        print(f"{self.__age}的{self.name}guangjie")

ls=Girl("ls",18)
print(ls.name)
print(ls._Girl__age) # 报错
ls._Girl__guangjie()# 报错
"""

"""
class Girl:
    def __init__(self, name, age):
        self.name = name
        self.__age = age

    @property  #方法转属性，不需要age()，而是直接age即可
    def age(self):
        if self.__age>=18:
            return 18
        else:
            return self.__age
    @age.setter
    def age(self, age):
        self.__age = age


ls = Girl("ls", 16)
# print(ls.get_age())
# ls.set_age(20)
# print(ls.get_age())
#属性私有化的一般写法【@property ，@age.setter】
print(ls.age)
ls.age=20
print(ls.age)
"""


# 注意：【@property装饰的方法不要和变量重名，否则可能导致无限递归】
# 一般方法命名：   私有属性去掉前面下划线
class Person:
    @property
    def name(self):
        return self.name


p = Person()
p.name
# 死递归，无限递归
