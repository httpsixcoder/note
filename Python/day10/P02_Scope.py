"""
    该案例演示了作用域
"""
""" 局部变量修改全局变量 global
num=10
def func():
    # num+=10 #b 报错
    # global num
    # num+=10
    print(num)

func()
print(num)
"""
# 闭包：
# 条件：
#       外部函数内定义一个内部函数
#       内部函数用到外部函数中的变量
#       外部函数将内部函数作为返回值
# 使用原因：函数调用结束后内部数据销毁，希望内部变量保留重复使用
# 作用：延长外部函数局部变量的生命周期

def outer():
    num=10
    def inner():
        nonlocal num
        num+=20
        print(num)
    inner()
    print(num)
outer()


