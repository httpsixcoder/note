"""
    该案例演示了多态
"""
class Animal:
    def go(self):
        pass
class Dog(Animal):
    def go(self):
        print("跑")
class Fish(Animal):
    def go(self):
        print("游")
class Bird(Animal):
    def go(self):
        print("飞")
def run(ani):
    ani.go()

"""
# 在方法的参数中使用多态
xh=Dog()
nm=Fish()
xm=Bird()
xh.go()
nm.go()
xm.go()
"""


def create_ani(flag):
    match flag:
        case 1:
            ani=Dog()
        case 2:
            ani=Fish()
        case 3:
            ani=Bird()
        case _:
            ani=None
    return ani
# 在返回值中使用多态
print(type(create_ani(1)))
print(type(create_ani(2)))
print(type(create_ani(3)))
print(type(create_ani(4)))
# 在声明变量的时候使用多态
dog=create_ani(1)
fish=create_ani(2)
bird=create_ani(3)
ani_list=[dog,fish,bird]
for ani in ani_list:
    ani.go()
