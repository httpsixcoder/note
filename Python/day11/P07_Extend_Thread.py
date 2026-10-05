"""
    该案例演示了继承Thread的子类实现线程
"""
import threading
import time


class Worder(threading.Thread):
    def run(self):
        flag=0
        while True:
            print(f"当前线程：{threading.current_thread().name}", f"{flag}" * 5)
            flag = flag ^ 1
            time.sleep(0.5)

if __name__=="__main__":
    t1=Worder(name="t1")
    t2=Worder(name="t2")
    t1.start()
    t2.start()
    print("end")