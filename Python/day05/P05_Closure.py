''''
    此案例演示了函数的闭包
'''

# 需求： 在一个函数中访问另一个函数中的变量
def func():
    num=10
    def inner(): 
        print(num)
    return inner
# func()()
inn=func()
inn()
inn()
inn()
# 闭包实现转装饰器
