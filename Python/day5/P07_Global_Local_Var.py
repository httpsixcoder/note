"""
    该案例演示了局部作用域修改全局变量
"""

num = 10


def func():
    # 当你在函数内部对一个变量进行赋值操作时，Python默认会把这个变量当作局部变量，即使是全局作用域中已经存在的同名变量
    # num=num+10 # 报错，找不到num
    global num  # 当前num即为全局作用域中的num【可以修改全局变量】
    num = 20
    print(num)


func()
print(num)


def outer():
    num1 = 100

    def inner():
        nonlocal num1 #当前变量不是局部变量【访问闭包作用域的变量，非全局变量，避免了global访问不到】
        num1 = 200
        print(num1)

    inner()
    print(num1)


outer()
