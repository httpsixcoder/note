"""
    该案例演示了raise
"""
"""
# 两个整数的加法计算【raise】
def add(a,b):
    if isinstance(a,int) and isinstance(b,int):
        return a+b
    else:
        raise TypeError("参数类型错误")
# print(add(3,4.0))
try:
    res=add(3,4.0)
except TypeError as e:
    print(type(e))
    print(e)
else:
    print(res)
"""

# assert
def int_add(x,y):
    assert isinstance(x,int) and isinstance(y,int),"参数类型错误"
    # assert 表达式：【相当于if not 表达式】
    return x+y
print(int_add(3,4.0))


