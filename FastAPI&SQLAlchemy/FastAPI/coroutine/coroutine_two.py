"""
    测试asyncio.run()：以同步的方式执行任务
"""
import asyncio
import time


# 创建协程函数
async def run(name, delay):
    print(f"任务{name}开始")
    await asyncio.sleep(delay)
    print(f"任务{name}完成")
    return f"任务{name}结果"


# 程序的入口函数
async def main():
    # await 协程对象：可以隐式的将协程对象注册为事件循环的一个任务
    await  run("A", 1)
    await  run("B", 2)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    # 耗时：3.02s
    print(f"耗时{end_time - start_time:.2f}s")
