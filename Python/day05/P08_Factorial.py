"""
    该案例演示了函数递归
"""


# 求5的阶乘

def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


factorial(5)
