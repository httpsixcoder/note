"""
    该案例演示了self
"""


class Student:
    school = "atguigu"

    def __init__(self, name):
        self.name = name

    def drink(self):
        print(f"{self.name}在{self.school}喝红牛")
        self.study()
        # 等价于
        # Student.drink(self)

    def study(self):
        print("努力学习")

gao=Student("gao")
gao.drink()
