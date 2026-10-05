"""
    该案例演示了进程之间不共享数据
"""
import os
from multiprocessing import Process


def func(list1):
    for i in range(3):
        list1.append(i)
        print(f"当前进程:{os.getpid()},数据：{list1}")

if __name__ == '__main__':
    list1=[]
    p1=Process(target=func,args=(list1,))
    p2=Process(target=func,args=(list1,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(list1)
    print("end")