# 每日一考
# ### 题目 1：动态添加属性
# 定义一个 Person 类，在类外动态地给 Person 类的一个对象添加一个 hobby 属性，值为 "reading"，并打印该属性。
import math
from abc import ABC, abstractmethod

class Person:
    pass
p=Person()
p.hobby="reading"
print(p.hobby)
# ### 题目 2：动态添加方法
# 定义一个 Circle 类，该类有一个 radius 属性。在类外定义一个函数 calculate_area，
# 功能是计算圆的面积（面积公式：\(S = π r^2），然后将这个函数动态地添加为 Circle 类的一个对象的方法，并调用该方法计算半径为 5 的圆的面积。
# （提示：可使用 types.MethodType）
import types
class Circle:
    def __init__(self,radius):
        self.radius=radius
def calculate_area(self):
    return 3.14*self.radius**2
r=Circle(5)
r.calculate=types.MethodType(calculate_area,r)
print(r.calculate())
# ### 题目 3：封装特性
# 定义一个 BankAccount 类，有一个私有属性 __balance（初始余额为 0），
# 提供一个 deposit 方法用于存钱，一个 withdraw 方法用于取钱，取钱时如果余额不足则打印提示信息。
class BankAccount:
    def __init__(self):
        self.__balance=0
    def deposit(self,money):
        self.__balance+=money
        return "已存款"
    def withdraw(self,money):
        if money>self.__balance:
            return "余额不足"
        else:
            self.__balance-=money
            return self.__balance
b1=BankAccount()
print(b1.deposit(100))
print(b1.withdraw(200))
print(b1.withdraw(20))
# ### 题目 4：多态特性
# 定义一个 Shape 类，有一个抽象方法 area（方法体为空）。
# 再定义 Rectangle 类和 Circle 类继承自 Shape 类，分别实现 area 方法计算矩形面积（长 × 宽）和圆的面积（\(\pi r^2\)）。
# 创建 Rectangle 和 Circle 类的对象，将它们放入一个列表中，遍历列表并调用每个对象的 area 方法。


# 抽象类：如果类中存在抽象方法，那么这个类就是抽象类，需要让这个类继承ABC【】
# 抽象方法：只需要声明这个方法，但是方法的具体实现不能完成，方法上加注@abstractmethod
# 注意：抽象类不能被实例化，如果子类继承了抽象父类，必须对抽象类中的父类方法进行实现，如果没有实现，那么子类也属于抽象类，不能被实例化
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    def area(self):
        return self.length * self.width
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2
list1=[Rectangle(4,5),Circle(3)]
for o in list1:
    print(o.area())
# ---------------------------------------------------------------------------------------------------------
### 编程题 1：数字反转
# 编写一个函数，接受一个整数作为参数，返回该整数的反转形式。例如，输入 123，返回 321；输入 -456，返回 -654。
def func1(n):
    sign=-1 if n<0 else 1
    return sign*int(str(abs(n))[::-1])
print(func1(123))
print(func1(-456))
### 编程题 2：嵌套字典数据处理
# 有一个嵌套字典，存储了学生的课程成绩信息。 编写一个函数，计算每个学生的平均成绩，并返回一个新的字典，键为学生名字，值为平均成绩。
# 结构如下：
students = {
    "Alice": {
        "Math": 85,
        "English": 90,
        "Science": 78
    },
    "Bob": {
        "Math": 92,
        "English": 88,
        "Science": 95
    },
    "Charlie": {
        "Math": 70,
        "English": 75,
        "Science": 80
    }
}
def func2(dict1):
    return {i:sum(v.values())/len(v.values()) for i,v in dict1.items()}
print(func2(students))

