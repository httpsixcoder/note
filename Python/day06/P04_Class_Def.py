"""
    该案例演示了类的定义
"""


class Person:
    """人的类"""
    # 类属性--会被当前类的所有实例（对象）共享
    home = "earth"

    # self 代表类创建出来的实例对象
    def __init__(self, name, age):
        # 实例属性--每一个实例独有
        self.name = name
        self.age = age

    # 实例方法
    def eat(self):
        print("eating")

    def drink(self):
        print("drinking")


"""# 访问类的成员
print(Person.__doc__) #打印类的说明文档
print(Person.home)
print(Person.eat)
print(Person.__init__)
"""
