"""
    该案例演示了单继承
"""


class Person:
    """人的类"""
    home = "earth"
    def __init__(self, name):
        self.name = name
    def eat(self):
        print("eating")

class YellowRacer(Person):
    color="yellow"
class OrangeRacer(Person):
    color="orange"
class GreenRacer(Person):
    color="green"

yr=YellowRacer("zs")
print(yr.color)
print(yr.name)
print(yr.home)
yr.eat()
print("-------------")
gr=GreenRacer("ls")
print(gr.color)
print(gr.name)
print(gr.home)
gr.eat()
print("-------------")
orp=OrangeRacer("ww")
print(orp.color)
print(orp.name)
print(orp.home)
orp.eat()
