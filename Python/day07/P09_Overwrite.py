"""
    该案例演示了方法的重写
"""
class Person:
    home="earth"
    def __init__(self,name):
        self.name=name
    def eat(self):
        print("eating...")
class Chinese(Person):
    color="yellow"
    # 重写
    # 【Java中有重写还有重载，但是Python中只有重写，因为在内存中，如果方法名一致，只对应一个地址，所以指挥按照最后一个执行】
    # 【在Python中实现重载，通过可变参数。eg: def eat(self，*args，**args)】
    def eat(self):
        print("用筷子吃")
y1=Chinese("zs")
y1.eat()