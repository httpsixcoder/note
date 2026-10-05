"""
    该案例演示了通过Process类创建进程对象
"""
import multiprocessing
import time


# 写
def write_file():
    print(f"write_file{__name__}")
    with open('./file.txt', 'w') as f:
        while True:
            f.write('hello world\n')
            # 文件写入时，数据先进入内存缓冲区，缓冲区满了才会真正写到硬盘。
            # 如果写进程不调用 f.flush()，读进程可能很长时间读不到新数据（因为数据还在内存里）。
            # f.flush() 强制将缓冲区数据立刻写入硬盘，让读进程能立刻读取到。
            f.flush()
            time.sleep(0.5)


def read_file():
    print(f"read_file{__name__}")
    with open('./file.txt', 'r') as f:
        while True:
            time.sleep(0.5)
            content = f.read()
            print(content)


# write_file()
# read_file()
p1=multiprocessing.Process(target=write_file)
p2=multiprocessing.Process(target=read_file)

# if __name__ == '__main__': 的必要性（重中之重！）
# 在 Windows 下，Python 创建新进程是通过重新导入当前模块来实现的。
# 如果不在 if __name__ == '__main__': 里调用 start()，那么新进程在导入模块时，
# 又会执行到 p1.start()，从而无限递归创建新进程，直接导致系统卡死或报 RuntimeError。
if __name__=='__main__':
    print(f"主进程{__name__}")
    p1.start()
    p2.start()

    print("end")