"""
    该案例演示了复用父类的成员
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
        # 调用父类方法
        # Person.eat(self) #self.ear()
        super().eat()
        print("studying...")

class ChineseStudent(Student, YellowRace):
    country="中国"
zs=ChineseStudent("zs","1年级")
zs.study()