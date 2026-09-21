"""
    该案例演示了方法
"""
"""
# 实例方法
# 实例方法在类中定义,第一个参数是self,代表实例本身
# 实例方法只能被实例对象所调用
# 可以访问实例属性,类属性,类方法
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def run(self):
        print(f"{self.brand}品牌的{self.color}的车在跑")

c=Car("小米","红色")
c.run()
"""

"""
# 类方法
# 在类中通过装饰器@classmethod 定义,第一个参数cls,代表类本身
# 可以被类和实例调用
# 可以访问类属性
# 在不创建实例的情况下,通过类名直接调用,方便,适合一些和类整体相关的操作
class Person:
    home = "earth"

    @classmethod
    def class_method(cls):
        print("class_method", cls.home, cls.__doc__)

    def run(self):
        pass


Person.class_method()

p = Person()
p.run()
"""
"""
# 静态方法
# 静态方法在类中通过装饰器 @staticmethod 定义
# 不访问实例属性或类属性,只依赖传入的参数
# 通过类名或实例调用,但它不会访问类或者实例的内部信息,更像是一个工具函数,只是为了方便组织代码,把他放在类里面

class Person:
    home = "earth"

    @classmethod
    def class_method(cls):
        print("class_method", cls.home, cls.__doc__)

    def fun(self):
        pass

    @staticmethod
    def mi():
        print("static_method")

Person.class_method()
Person.mi()
"""


# 魔法方法
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 一般给程序员看的
    def __str__(self):
        return f"Name;{self.name};{self.age}"

    # 一般对系统友好的,可以拿来直接用的
    def __repr__(self):
        return f"Person('{self.name}',{self.age})"
    # def __del__(self):
    #     print("del被调用")

    # 和其它对象比较 运算符的重载
    def __lt__(self, other):
        return self.age < other.age


# p1 = Person()
# p2 = p1
# del p1
# del p2
p1=Person("zs",20)
# # print("end")
# print(p1) #<__main__.Person object at 0x000002860C67B620>
# print(str(p1)) #<__main__.Person object at 0x000002860C67B620> 底层调用__str__
# # 修改默认__str__后
# print(p1) # Name;zs;20
# print(str(p1)) # Name;zs;20
# zz=eval(repr(p1))
# print(type(zz)) #<class '__main__.Person'>
p2=Person("ls",20)
print(p1>p2)
