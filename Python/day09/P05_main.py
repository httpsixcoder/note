"""
    该案例演示了带包导入
"""
"""
# 全局导入——导入包下某个模块的所有成员
import graphic.circle
import graphic.rectangle as rec
print(graphic.circle.area())
print(graphic.circle.perimeter())
print(rec.area())
print(rec.perimeter())
# 全局导入——导入包下所有模块
import graphic
print(graphic.circle.area())
"""
"""
# 局部导入——方式1 导入包中每个模块
from graphic import circle as circ
print(circ.area())

# 局部导入——方式2 导入包中模块的某一个成员
from graphic.circle import area as circ_area
print(circ_area())
"""

# from graphic.circle import *
# print(area())
from graphic import *
print(circle.area())