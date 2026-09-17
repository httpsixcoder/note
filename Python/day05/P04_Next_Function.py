'''
    该案例演示了函数的嵌套调用
'''

def fun1(num):
    print("func1执行")
    print(num)
    print("func1结束")

def fun2(num):
    print("func2执行")
    num=10
    fun1(num)
    print("func2结束")

fun2(10)
# 函数进栈
# 打印fun2函数中的变量，需要调用fun1