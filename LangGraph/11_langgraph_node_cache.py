"""
    测试：节点缓存
    1.添加节点时，设置缓存策略,cache_policy
    ttl:表示缓存的过期时间，单位为秒，不设置则表示用不过期
    builder.add_node(expensive_node, cache_policy=CachePolicy(ttl=10))  # 10s
    2.在编译得到图对象时，设置缓存存储的位置
    graph = builder.compile(cache=InMemoryCache())
    3.注意：
    缓存的本质是键值对，存储键默认的情况下使用pickle对输入进行hash运算的结果
    因此要想缓存命中，必须保持输入（状态）一致
    【输入一致 -> 键一致 -> 命中缓存】
"""
import time
from typing import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy


class MyState(TypedDict):
    x: int
    result: int


def expensive_node(state: MyState):
    print("expensive node开始执行")
    time.sleep(3)
    print("expensive node结束执行")
    return {"result": state["x"] * 2}


builder = StateGraph(MyState)
builder.add_node(expensive_node, cache_policy=CachePolicy(ttl=10))  # 10s

builder.set_entry_point("expensive_node")

graph = builder.compile(cache=InMemoryCache())

# 第一次调用
result1 = graph.invoke({"x": 5})
print(result1)

# 第二次调用
result2 = graph.invoke({"x": 5})
print(result2)
