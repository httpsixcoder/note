"""
    该案例演示了多继承
"""


class Person:
    home = "earth"

    def __init__(self, name):
        self.name = name

    def eat(self):
        print("eating")


class YellowRacer(Person):
    color = "yellow"

    def __init__(self):
        print("xxx")

    def run(self):
        print("running")


class Student(Person):
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        # Person.__init__(self,name)

    def study(self):
        print("studying")


class ChineseStudent(Student, YellowRacer):
    country = "china"
    

cs = ChineseStudent("zs", "1年纪")
print(cs.country)
print(cs.name)
print(cs.grade)
print(cs.color)
print(cs.home)
cs.study()
cs.run()
cs.eat()
