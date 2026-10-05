"""
    售票案例
"""
import threading
import time


def func():
    global ticket_num
    # 锁加在这合这（循环外），就只有一个人能买到票
    while True:
        lock.acquire()
        if ticket_num <= 0:
            lock.release()
            break
        time.sleep(0.1)
        ticket_num -= 1
        print(f"{threading.current_thread().name}卖了1张票,还剩{ticket_num}张")
        # 锁加在这合这（break下面），最后一次判断break永远不释放锁，程序一直执行
        # lock.release()

if __name__ == '__main__':
    ticket_num = 100

    lock = threading.Lock()
    # 创建线程对象
    thread_list = [threading.Thread(target=func,name="窗口" + str(i)) for i in range(3)]

    [t.start() for t in thread_list]
    [t.join() for t in thread_list]