"""
    思考题
"""

class Person:
    aa="hello"
    def __init__(self):
        self.aa="world"
    #
    # def __init__(self,name):
    #     self.name=name
    # # 会覆盖掉前两个init函数
    # def __init__(self,name,age):
    #     self.name=name
    #     self.age=age

    def aa(self):
        print("welcome")

p=Person()
print(p.aa)         # world
# p.aa()            # 报错
print(Person.aa)    #function