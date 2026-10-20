"""
    测试:以异步的方式执行协程函数
    1.常用方法
            async.create_task()：将写成对象创建成为事件循环中的一个任务
            asyncio.gether(task1,task2,...)：异步执行多个任务
            asyncio.run()：启动协程
    2.一般执行协程函数时，都需要设置一个入口函数（顶级协程对象），统一管理其他协程函数的执行
    若执行协程函数时，入口函数（顶级协程对象）提前退出，则整个事件循环结束
    3.将一个协程函数注册为任务，有两种方式：
        a-> asyncio.create_task(fun())
        b-> asyncio.gather(fun(),fun(),):隐式将协程对象注册为任务
"""
import asyncio
import time
from unittest import result


# 创建协程函数
async def run(name, delay):
    print(f"任务{name}开始")
    await asyncio.sleep(delay)
    print(f"任务{name}完成")
    return f"任务{name}结果"


# 程序的入口函数（顶级协程对象）
async def main():
    # 将携程对象注册为事件循环中的任务
    # task1=asyncio.create_task(run("A",1))
    # task2=asyncio.create_task(run("B",2))
    # 以异步的方式执行任务
    # result=await asyncio.gather(task1,task2)
    # ['任务A结果', '任务B结果']【结果】

    # result=await asyncio.gather(run("A",1),run("B",2))
    result=await asyncio.gather(
        run("A",1),run("B",2)
    )
    print(result)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    # 耗时2.01s
    print(f"耗时{end_time - start_time:.2f}s")
