"""
    该案例演示了实例化对象
"""


class Student:
    """学生类"""
    # 类属性
    school = "atguigu"

    def __init__(self, name, age):
        # 定义实例属性
        self.name = name
        self.age = age

    def study(self):
        print("学习中...")

    def eat(self):
        print("吃饭中...")


# 创建对象（实例化）  --- 底层调用__init__方法
gao = Student("gao", '18')

print(gao.school)
print(gao.name)
print(gao.age)

# Student.eat(gao)
# 语法糖
gao.study()
