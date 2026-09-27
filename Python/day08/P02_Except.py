"""
    该案例演示了语法的错误和异常
"""
"""
# 语法错误 程序对语法进行解析阶段就发现问题 程序不会执行
def fun1():
    print("hello")
    while True print(1)
fun1()
"""
"""
# 程序的语法正确，在运行他的时候，也可能发生错误。运行期间检测到的错误成为异常
def fun1():
    print("hello")
    print(a)
fun1()
"""
# 如果不对程序运行的过程中发生的异常进行处理，程序默认的处理方式是将异常打印到控制台
# 程序也会终止，异常后面的代码不会被执行

# 异常处理
# res=3/1
try:
    res=3/0
    # res=3/1
    print(res)
except:
    print("发生了异常")
print("end")
