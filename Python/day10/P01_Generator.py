"""
    该案例演示了生成器
"""
import time

"""
# 生成器对象创建方式1:推导式
gen=(i for i in range(3))
print(type(gen))
# for i in gen:
#     print(i)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
"""

"""
# 生成器对象创建方式2:生成器函数
# 版本1:斐波那契 for循环
def fibo():
    a, b = 0, 1
    while True:
        a, b = b, a + b
        print(b)
        # time.sleep(1)
fibo()
# 版本2:自定义迭代器生成 斐波那契
class MyIter:
    def __init__(self):
        self.a = 0
        self.b = 1
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.b
it = MyIter()
print(type(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))
# 版本3：生成器函数
# 主要在函数体中出现了yield关键字，那么这个函数就是生成器函数，当这个函数执行后，返回值类型就是生成器类型对象
def fibo():
    a, b = 0, 1
    while True:
        a, b = b, a + b
        yield b
f=fibo()
print(next(f))
print(next(f))
print(next(f))
print(next(f))

# 如何获得函数的返回值
def fibo(n):
    a, b,count = 0, 1,0
    while count<n:
        a, b,count = b, a + b,count+1
        yield b
    return "函数执行完毕"
f=fibo(3)
print(type(f))
# 底层如果next没有返回值，则 raise StopIteration异常 把return内容当作异常信息返回
try:
    while True:
        print(next(f))
except StopIteration as e:
    print(e.value)

# 向生成器函数发送数据
# 需求：使用send()发送任务id，使生成器交替执行两个任务
def func():
    int_value = 0
    chr_value = "A"
    task_id=1
    while True:
        match task_id:
            case 1:
                int_value += 1
                task_id=yield int_value
            case 0:
                chr_value=chr(ord(chr_value)+1)
                task_id = yield chr_value
            case _:
                task_id=yield
f1=func()
print(next(f1))
print(f1.send(1))
print(f1.send(1))
print(f1.send(1))
print(f1.send(0))
print(f1.send(0))
print(f1.send(0))
"""
# 通过send启动生成器
def func():
    int_value = 0
    chr_value = "A"
    task_id=1
    while True:
        match task_id:
            case 1:
                int_value += 1
                task_id=yield int_value
            case 0:
                chr_value=chr(ord(chr_value)+1)
                task_id = yield chr_value
            case _:
                task_id=yield
f1=func()
# print(f1.send(1))
print(f1.send(None))
