"""
    该案例演示了线程安全问题
"""
"""
# 线程安全问题演示
import threading
import time
from concurrent.futures import thread
def func1():
    global num
    for _ in range(10):
        # num += 1
        temp=num+1
        time.sleep(0.1)
        num=temp
        print(f"{threading.current_thread()}:{num}")
if __name__ == "__main__":
    num=0
    thread_list= [threading.Thread(target=func1,name="线程"+str(i)) for i in range(3)]
    [t.start() for t in thread_list]
    [t.join() for t in thread_list]
    print(num)
"""
# 解决【互斥锁】
import threading
import time
def func1():
    # 在这加锁会变成同步操作
    # lock.acquire()
    global num
    for _ in range(10):
        # 在这加锁会才是异步操作
        lock.acquire()
        temp=num+1
        time.sleep(0.1)
        num=temp
        print(f"{threading.current_thread()}:{num}")
        lock.release()
if __name__ == "__main__":
    num=0
    lock=threading.Lock()
    thread_list= [threading.Thread(target=func1,name="线程"+str(i)) for i in range(3)]
    [t.start() for t in thread_list]
    [t.join() for t in thread_list]
    print(num)