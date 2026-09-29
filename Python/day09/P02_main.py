"""
# 全局导入
import P01_my_add
print(P01_my_add.num)
print(P01_my_add.add(10, 20))
# 给导入模块取别名
import P01_my_add as ma
print(ma.num)
print(ma.add(10, 20))
"""
"""
# 局部导入，方式1：导入模块的部分成员
from P03_my_multi import  multi,_str1,num
from P01_my_add import  num
# print(_str1)
# 只能访问导入的成员，没有导入的成员不能访问
# print(num)
# print(multi(5,10))
# 如果导入多个模块有重名的成员，会进行覆盖，以最后一次导入为准，可以通过设置不同的重名，都使用
print(num)
"""
"""
# 局部导入，方式2：导入模块中所有不以单下划线开头的成员
from P03_my_multi import  *
print(num)
# 在被导入文件中设置了__all__，只可以访问__all__列表中的成员
# print(multi(5,10))
# print(_str1)
"""
# 测试__name__
# from P01_my_add import  *

# dir()
# import math
# print(dir(math))
#
# class MyClass():
#     def __init__(self):
#         self.x = 10
#         self.y = 20
#     def func(self):
#         pass
# mc1=MyClass()
# print(dir(mc1))

# def func():
#     pass
# variable=10
# # 打印当前模块作用域内有哪些成员【变量，函数，类】
# print(dir())

