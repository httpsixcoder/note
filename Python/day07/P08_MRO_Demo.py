"""
    该案例演示了MRO以及super结合使用
"""
"""
class Parent1:
    def __init__(self,value1):
        print("Initializing Parent1")
        self.value1=value1

class Parent2:
    def __init__(self,value2):
        print("Initializing Parent2")
        self.value2=value2
# 子类中重复初始化
# class Child1(Parent1,Parent2):
#     def __init__(self,value1,value2):
#         print("Initializing Child3")
#         self.value1=value1
#         self.value2=value2

# #复用父类的方法，对value1和value2进行初始化————父类名.方法名()
# class Child1(Parent1,Parent2):
#     def __init__(self,value1,value2):
#         print("Initializing Child")
#         Parent1.__init__(self,value1)
#         Parent2.__init__(self,value2)
# c=Child1(1,2)
# print(c.value1)
# print(c.value2)

#复用父类的方法，对value1和value2进行初始化————super().方法名()
# 代码报错super调用的都是Parent1，value没有赋值
# class Child1(Parent1,Parent2):
#     def __init__(self,value1,value2):
#         print("Initializing Child")
#         super().__init__(value1)
#         super().__init__(value2)
# print(Child1.__mro__)
# c=Child1(1,2)
# print(c.value1)
# print(c.value2)

#复用父类的方法，对value1和value2进行初始化————super().方法名()
# 进阶，但是当继承的类Parent1和Parent2调换位置后还会报错
class Child1(Parent1,Parent2):
    def __init__(self,value1,value2):
        print("Initializing Child")
        super().__init__(value1)
        #super(MRO中的类，实例对象).__init__()->显式指定“从哪个类的下一个位置开始查找”
        super(Parent1,self).__init__(value2)
print(Child1.__mro__)
c=Child1(1,2)
print(c.value1)
print(c.value2)
"""
"""
# 另外一种写法，更为适用
class Parent1:
    def __init__(self,value1,**args):
        print("Initializing Parent1")
        self.value1=value1
        super().__init__(**args)

class Parent2:
    def __init__(self,value2,**args):
        print("Initializing Parent2")
        self.value2=value2
        super().__init__(**args)

class Child1(Parent2,Parent1):
    def __init__(self,value1,value2):
        print("Initializing Child")
        super().__init__(value1=value1,value2=value2)
c=Child1(1,2)
print(c.value1)
print(c.value2)
"""

"""
class A:
    def __init__(self,a,b,c,**args):
        print("Initializing A")
        self.a=a
        self.b=b
        self.c=c
        super().__init__(**args)
class B:
    def __init__(self,d,e,f,**args):
        print("Initializing B")
        self.d=d
        self.e=e
        self.f=f
        super().__init__(**args)
class C(A,B):
    def __init__(self,a,b,c,d,e,f):
        # 方法一：
        # A.__init__(self,a,b,c)
        # B.__init__(self,d,e,f)
        # 方法二：
        super().__init__(a=a,b=b,c=c,d=d,e=e,f=f)
"""


class GrandParent:
    def __init__(self):
        print("Initializing GrandParent")


class Parent1(GrandParent):
    def __init__(self):
        super().__init__()
        print("Initializing Parent1")


class Parent2(GrandParent):
    def __init__(self):
        super().__init__()
        print("Initializing Parent2")

# 方法一：基类调用两次__init__
# class Child(Parent1, Parent2):
#     def __init__(self):
#         Parent1.__init__(self)
#         Parent2.__init__(self)
# 方法二：按照ROM去执行【解决继承的钻石问题】
class Child(Parent1, Parent2):
    def __init__(self):
        super().__init__()

Child()
# Initializing GrandParent
# Initializing Parent2
# Initializing Parent1
# Initializing GrandParent
# Initializing Parent2