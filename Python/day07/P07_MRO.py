"""
    该案例演示了方法的解析顺序
"""

class Person:
    home="earth"
    def __init__(self,name):
        self.name=name
    def eat(self):
        print("eating...")
class YellowRace(Person):
    color="yellow"
    def run(self):
        print("running...")
class Student(Person):
    def __init__(self,name,gender):
        self.name=name
        self.gender=gender
    def study(self):
        print("先吃在学")
        Person.eat(self) #self.ear()
        # super().eat()
        print("studying...")

class ChineseStudent(Student, YellowRace):
    country="中国"
zs=ChineseStudent("zs","1年级")
print(ChineseStudent.__mro__) #调用顺序
# 打印：
# (<class '__main__.ChineseStudent'>,
# <class '__main__.Student'>,
# <class '__main__.YellowRace'>,
# <class '__main__.Person'>,
# <class 'object'>)
