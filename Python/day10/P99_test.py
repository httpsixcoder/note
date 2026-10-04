"""
    每日一考
"""
from vehicle.car import Car

### 一、操作题
# 各组组长：
# 1.定义一个包，包名为vehicle，在包下定义一个模块，模块名为car.py，
# 在模块下定义一个Car类，类中提供start，stop方法，
# 方法中分别打印输出start和stop。
# 2.打包
# 各组组员：
# 将组长打好的包安装到pycharm中，并创建测试模块，
# 创建一个车对象，并调用start和stop方法。
# 答案参考笔记中的打包和安装
# 组长:
"""
# setup of file:
# 新版本
from setuptools import setup
setup(
    name='vehicle',
    version='1.0',
    py_modules=['vehicle.car'],
)
# pip install build
# /python -m build
"""
"""
# 组员:
# pip install .\dist\vehicle-1.0-py3-none-any.whl
from vehicle import car
# 测试
if __name__ == '__main__':
    c1=Car("红旗")
    print(c1)
    print(c1.name)
    c1.start()
    c1.stop()
"""