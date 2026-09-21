"""
    案例演示了属性
"""

"""
# 类属性
class Person:
    home = "earth"  # 定义类属性


# 访问：类名.属性名 或者 实例.属性名
gao = Person()
print(gao.home)
print(Person.home)

# # 添加、修改类属性 类名.属性名=值
# Person.home="地球"
# print(Person.home)

gao1 = Person()
gao1.home = "地球"
print(gao1.home)
print(gao.home)
"""

# 实例属性
class Person:
    def __init__(self, name):
        self.name = name
zs=Person('zs')
print(zs.name)
zs.name = 'zsf'

zs.age = 20
print(zs.name)
print(zs.age)
print("----------------")
ls=Person('ls')
print(ls.name)
# print(ls.age) # 报错没有