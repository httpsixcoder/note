"""
    该案例演示了自定义异常
"""

class MyException(Exception):
    pass

# 接收一个年龄参数，打印到控制台
def get_age(age):
    if age >= 200 or age <=0:
        raise MyException("年龄不合法")
    print(age)
get_age(-5)