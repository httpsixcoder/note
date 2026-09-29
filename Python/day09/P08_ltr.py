"""
    该案例演示了迭代器
"""
from collections.abc import Iterable
from typing import Iterator

"""
import os

for element in[1,2,3]:
    print(element)
for element in (1,2,3):
    print(element)
for key in {"one":1,"two":2}:
    print(key)
for char in "123":
    print(char)

with open("myfile.txt",'w') as f:
    f.write("h\ne\nl\nl\no\n")
for line in open("myfile.txt"):
    print(line,end='')
os.remove("myfile.txt")
"""
"""
#  判断对象是否可以得迭代
print(isinstance([],Iterable))
print(isinstance((),Iterable))
print(isinstance(set(),Iterable))
print(isinstance({},Iterable))
print(isinstance("100",Iterable))
print(isinstance(100,Iterable)) #False

"""
"""
#  判断对象是否为迭代器
print(isinstance([],Iterator))
print(isinstance((),Iterator))
print(isinstance(set(),Iterator))
print(isinstance({},Iterator))
print(isinstance("100",Iterator))
print(isinstance((x for x in range(10)),Iterator)) #True
"""
"""
class MyT:
    def __iter__(self):
        print("11111")
        return self
    def __next__(self):
        print("22222")
        return  1
mt=MyT()
# print(isinstance(mt, Iterable))#是不是可迭代对象
# iter(mt)
print(isinstance(mt, Iterator)) #是不是迭代器
"""

"""
list1=[1,2,3]
# print(isinstance(list1, Iterator),type(list1))
aa=iter(list1)
# print(type(aa))
# print(isinstance(aa, Iterable),type(aa))
print(next(aa))
print(next(aa))
print(next(aa))
print(next(aa)) # 异常 StopIteration
"""

# 手动实现迭代器
class my_list_iterator:
    def __init__(self,lst):
        self.lst=lst
        self.index=0
    def __next__(self):
        if self.index==len(self.lst):
            raise StopIteration
        res=self.lst[self.index]
        self.index+=1
        return res

class my_list:
    def __init__(self,data):
        self.data=data
    def __iter__(self):
        return my_list_iterator(self.data)
ml=my_list([1,2,3])
# print(isinstance(ml,Iterable))
# ml_it=iter(ml)
# print(type(ml_it))
# print(next(ml_it))
# print(next(ml_it))
# print(next(ml_it))
for i in ml:
    print(i)









