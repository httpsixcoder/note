"""
    该案例演示通过队列实现了进程间的通信
"""
import os
import random
import time
from logging import Manager
from multiprocessing import Process,Pool,Queue,Manager



def func_put(queue):
    while True:
        num=random.randint(1,10)
        queue.put(num)
        print(f"进程{os.getpid()}向队列中放数据：{num}")
        time.sleep(0.5)
def func_get(queue):
    while True:
        value=queue.get()
        print(f"进程{os.getpid()}从队列中取数据：{value}")
        time.sleep(0.5)

if __name__ == '__main__':
    # 1.正常操作
    # queue =Queue(10)
    # p1=Process(target=func_put, args=(queue,))
    # p2=Process(target=func_get, args=(queue,))
    # p1.start()
    # p2.start()
    # 2.Pool进程池方式实现 【multiprocessing.Manager().Queue配合进程池中的apply_async】【兼容性】
    # pool = Pool(4)
    # queue =Manager().Queue(10)
    # pool.apply_async(func_put, args=(queue,))
    # pool.apply_async(func_get, args=(queue,))
    # pool.close()
    # pool.join()
    # print("end")
    # 3.前两种结合使用，需要在最后阻塞【p1.join()】【兼容性】
    queue =Manager().Queue(10)
    p1=Process(target=func_put, args=(queue,))
    p2=Process(target=func_get, args=(queue,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()