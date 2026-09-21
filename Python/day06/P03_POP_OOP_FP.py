"""
    该案例演示了面向过程,面向对象以及面向函数对比
"""

"""
# POP 面向过程
# 以步骤/过程为中心 怎么做
num1=10
num2=20
print(f"{num1}和{num2}的和是{num1+num2}")
print(f"{num1}和{num2}的差是{num1-num2}")
print(f"{num1}和{num2}的积是{num1*num2}")
print(f"{num1}和{num2}的商是{num1//num2}")
"""

"""
# OOP 面向对象
# 万物皆对象 谁来做
class Calculator:
    def add(self,num1,num2):
        return num1+num2
    def sub(self,num1,num2):
        return num1-num2
    def mul(self,num1,num2):
        return num1*num2
    def div(self,num1,num2):
        return num1//num2
zsCalc=Calculator()
print(zsCalc.add(10,20))
print(zsCalc.sub(10,20))
print(zsCalc.mul(10,20))
print(zsCalc.div(10,20))
"""

"""
# FP 面向函数变成
# 函数是第一公民 做什么
def add(num1,num2):
    return num1+num2
def sub(num1,num2):
    return num1-num2
def mul(num1,num2):
    return num1*num2
def div(num1,num2):
    return num1//num2
    
def calculate(num1,num2,op):
    return op(num1,num2)

calculate(10,20,op=add)
calculate(10,20,op=sub)
calculate(10,20,op=mul)
calculate(10,20,op=div)
"""