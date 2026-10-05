"""
    该案例演示了通过自定义类继承Process创建进程对象
"""
import os
from multiprocessing import Process


class Worker(Process):
    # start()做的事：创建子进程 → 在子进程中调用run()
    def run(self): #start->run->target
        print(f"进程号是：{os.getpid()}，父进程号是{os.getppid()}")

# 避免递归创建子进程
if __name__ == '__main__':
    print(f"进程号是：{os.getpid()}，父进程号是{os.getppid()}")
    w1=Worker()
    w2=Worker()
    # 如果你手动调用 w1.run()，它只是在当前进程执行 run() 里的代码，根本不会创建新进程。
    w1.start()
    w2.start()