"""
    每日一考
"""
# 1.创建一个简单的Python模块math_operations.py，其中定义两个函数add和multiply，分别用于实现两个数的加法和乘法运算。
# 在另一个Python文件中导入该模块，并调用这两个函数计算3 + 5和3 * 5的结果。
from math_operations import *
result_add=add(10, 20)
result_multiply=multiply(10,20)
print(result_add)
print(result_multiply)
# 2.使用生成器表达式创建一个生成器，生成1到10的偶数。然后使用for循环遍历该生成器，打印每个偶数。
generator1=(x for x in range(1,11) if x%2==0)
for v in generator1:
    print(v,end=" ")
print()
# 3.创建一个迭代器类MyIterator，用于遍历一个给定列表的元素。
#实现__iter__和__next__方法。使用该迭代器类遍历列表[10, 20, 30, 40]，并打印每个元素。
class MyIterator:
     def __init__(self,data):
         self.data = data
         self.index = 0
     def __iter__(self):
         return self
     def __next__(self):
         if self.index>=len(self.data):
             raise StopIteration
         value=self.data[self.index]
         self.index+=1
         return value
list1=[10, 20, 30, 40]
iterator1=MyIterator(list1)
for i in iterator1:
    print(i)