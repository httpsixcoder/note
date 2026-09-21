
class Person:
    # def __init__(self,):
        # __init__() should return None, not 'int'
        # return 10

    def eat(self):
        print("eating")

p=Person()
p.name="gao"
print(p.name)
# p.eat() 相当于 【底层执行】Person.eat(p)
p.eat()
Person.eat(p)
