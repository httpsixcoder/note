"""
    该案例演示了进程池
"""
import os
import time
import multiprocessing
def func():
    for i  in range(3):
        print(f"当前进程:{os.getpid()},打印:{i}")
        time.sleep(0.3)
if __name__=="__main__":
    process_num=5
    pool = multiprocessing.Pool(process_num)
    for i in range(process_num):
        # pool.apply(func) # 阻塞【同步】
        pool.apply_async(func) # 非阻塞【异步】
    # 处理报错Pool is still running
    # join() 要求池已经关闭，否则它不知道“什么时候算结束”。
    pool.close()
    # 守护进程，需要阻塞
    pool.join()
    print("end")
