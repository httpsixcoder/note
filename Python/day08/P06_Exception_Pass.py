"""
    该案例演示了异常的传递
"""
"""
# 方式一
try:
    try:
        try:
            print(3/0)
        except NameError:
            print("第一层")
    except ValueError:
        print("第二层")
except ZeroDivisionError:
    print("第三层")
"""

def m3():
    print(3/0)
def m2():
    m3()
def m1():
    m2()
m1()