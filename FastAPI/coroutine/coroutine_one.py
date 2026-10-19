"""
    测试：写协程的核心，async和await关键字
    1.由async修饰的函数返回一个协程对象
    2.模拟阻塞
    time.sleep()：阻塞线程
    async.sleep()：不会阻塞线程
    因此在协程中，若需要模拟阻塞操作，一定不能用time.sleep()
    3.async修饰函数中，阻塞操作是可选的，即协程函数中可有await也可以没有
    await不能单独使用，即await必须出现在协程函数中
    4.直接调用协程函数不会执行，而是返回一个协程对象，需要使用asyncio.run()启动协程
"""
import asyncio


async def fun():
    print("hello")
    await asyncio.sleep(2)
    print("world")


if __name__ == "__main__":
    # result = fun()
    # <coroutine object fun at 0x0000017415459B40> 协程对象
    # print(result)
    asyncio.run(fun())
