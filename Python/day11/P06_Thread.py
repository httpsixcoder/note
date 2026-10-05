"""
    该案例演示了Thread创建线程
"""
import threading
import time

def func():
    flag=0
    while True:
        print(f"当前线程：{threading.current_thread().name}",f"{flag}"*5)
        flag=flag ^ 1
        time.sleep(0.5)

if __name__=="__main__":
    t1=threading.Thread(target=func,name="t1")
    t2=threading.Thread(target=func,name="t2")
    t1.start()
    t2.start()
