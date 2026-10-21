from asyncio import CancelledError

import anyio

# 用来控制最大并发数量
sem = anyio.Semaphore(10)


async def fetch_data(name, delay):
    print(f"任务 {name} 开始")
    await anyio.sleep(delay)
    print(f"任务 {name} 完成")
    return f"任务 {name} 结果"


# 带并发限流 + 异常捕获的包装层
async def run_limited(name, delay):
    try:
        # `async with` 是异步上下文管理器。进入的时候申请信号量许可，退出的时候自动释放许可。
        async with sem:
            return {"ok": True, "name": name, "data": await fetch_data(name, delay)}
    except CancelledError:
        # 单独捕获取消异常（超时、外部取消都会抛这个）
        return {"ok": False, "name": name, "err": "任务被取消/全局超时"}
    except Exception as e:
        return {"ok": False, "name": name, "err": str(e)}


# 顶级函数
async def main():
    results = []
    # （任务组），结构化并发核心。主协程一定会等待所有子任务全部完成
    async with anyio.create_task_group() as tg:
        #  tg.start_soon
        for i in range(20):
            # 👉 经典闭包陷阱修复！
            async def wrapper(idx=i):
                r = await run_limited(f"Task-{idx}", 1)
                results.append(r)

            # 一次性把 20 个任务全部交给 TaskGroup 调度
            tg.start_soon(wrapper)
        # 正确写法：当前时间往后5.5秒截止
        tg.cancel_scope.deadline = anyio.current_time() + 2.0
    for mes in results:
        print(mes)


if __name__ == '__main__':
    anyio.run(main)
