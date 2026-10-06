# ### 一、选择题
# 1. 在 Python 中，以下关于进程和线程的说法，正确的是（ C ）
# A. 进程之间共享内存空间，线程之间不共享      B. 创建进程比创建线程开销更小
# C. 一个进程可以包含多个线程      D. 线程不能并发执行，进程可以并发执行
# 2. 以下哪个模块用于在 Python 中创建进程？（ B ）
#    A. threading  B. multiprocessing	C. os	D. sys
# ### 二、编程题
# 1. 使用multiprocessing模块创建两个进程，一个进程打印从 1 到 5 的数字，另一个进程打印从 6 到 10 的数字。
import multiprocessing
import threading
def func1(start,stop):
    for i in range(start, stop+1):
        print(i)
# 2. 使用threading模块创建两个线程，一个线程打印 10 次 "Hello"，另一个线程打印 10 次 "World"。
def func2(str):
    for i in range(10):
        print(f"{str}")
if __name__ == '__main__':
    m1 = multiprocessing.Process(target=func1(1,5))
    m2 = multiprocessing.Process(target=func1(6,10))
    m1.start()
    m2.start()
    m1.join()
    m2.join()
    t1 = threading.Thread(target=func2("hello"))
    t2 = threading.Thread(target=func2("world"))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

"""
### 一、选择题
1. 在 Python 中，以下关于进程和线程的说法，正确的是（  ）
A. 进程之间共享内存空间，线程之间不共享
B. 创建进程比创建线程开销更小
C. 一个进程可以包含多个线程
D. 线程不能并发执行，进程可以并发执行
**答案**：C
**分析**：
进程有独立的内存空间，进程之间不共享内存，而线程共享所属进程的内存空间，选项 A 错误。
创建进程需要分配独立的内存等资源，创建线程只需在所属进程的内存空间内进行资源分配，所以创建进程比创建线程开销更大，选项 B 错误。
一个进程可以包含多个线程，这些线程共享进程资源，选项 C 正确。
在多核心 CPU 环境下，进程和线程都可以并发执行，选项 D 错误。
2. 以下哪个模块用于在 Python 中创建进程？（  ）
A. threading
B. multiprocessing
C. os
D. sys
**答案**：B
**分析**：
threading模块用于创建和管理线程，选项 A 错误。
multiprocessing模块用于在 Python 中创建进程，提供了创建、管理进程的各种功能，选项 B 正确。
os模块主要用于与操作系统进行交互，如文件操作、进程管理等，但不是专门用于创建进程的模块，选项 C 错误。
sys模块主要用于访问 Python 解释器相关的变量和函数，与创建进程无关，选项 D 错误。
### 二、编程题
1. 使用multiprocessing模块创建两个进程，一个进程打印从 1 到 5 的数字，另一个进程打印从 6 到 10 的数字。
**答案**：
```python
import multiprocessing
def print_numbers1():
    for i in range(1, 6):
        print(f"进程1: {i}")
def print_numbers2():
    for i in range(6, 11):
        print(f"进程2: {i}")
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=print_numbers1)
    p2 = multiprocessing.Process(target=print_numbers2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```
**分析**：首先定义了两个函数print_numbers1和print_numbers2，分别用于打印从 1 到 5 和从 6 到 10 的数字。在if __name__ == '__main__':代码块中，创建了两个进程p1和p2，分别指定它们的执行目标为print_numbers1和print_numbers2。调用start()方法启动进程，join()方法用于等待进程执行结束，确保程序不会提前退出，展示了使用multiprocessing模块创建和管理进程的过程。
2. 使用threading模块创建两个线程，一个线程打印 10 次 "Hello"，另一个线程打印 10 次 "World"。
**答案**：
```python
import threading
def print_hello():
    for _ in range(10):
        print("Hello")
def print_world():
    for _ in range(10):
        print("World")
if __name__ == '__main__':
    t1 = threading.Thread(target=print_hello)
    t2 = threading.Thread(target=print_world)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
```
**分析**：定义了print_hello和print_world两个函数，分别用于打印 10 次 "Hello" 和 "World"。在if __name__ == '__main__':代码块中，创建两个线程t1和t2，将print_hello和print_world作为线程执行的目标函数。调用start()方法启动线程，join()方法等待线程执行完毕，展示了使用threading模块创建和管理线程的过程。
"""
