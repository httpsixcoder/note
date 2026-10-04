# 方法一：相对路径【推荐】
from . import circle
# 方法二:绝对路径
# from python.day09.graphic import circle
# 错误【模块查找照顺序，当前目录针对的是直接执行文件的目录】
# import circle
# 方法三：【注意一定要用别名，这样导入该模块的那个文件可以直接使用别名】
# import day09.graphic.circle as circle

#
# __all__=["circle"]

