# from distutils.core import setup
from setuptools import setup

setup(
    name='graphic',     #需要打包的名字
    version='1.0',      #版本
    py_modules=["graphic.circle","graphic.rectangle"],  #需要打包的模块
)