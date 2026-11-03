"""
    测试：获取图对象的节点、通道、节点的订阅和写入
"""
import operator
from typing import TypedDict, Annotated, List

from langgraph.constants import END
from langgraph.graph import StateGraph


# 创建状态类
class MyState(TypedDict):
    aggregate: Annotated[List[str], operator.add]


# 创建节点
def node_a(state: MyState):
    return {"aggregate": ["A"]}


def node_b(state: MyState):
    return {"aggregate": ["B"]}


def node_c(state: MyState):
    return {"aggregate": ["C"]}


def node_b2(state: MyState):
    return {"aggregate": ["B2"]}


def node_d(state: MyState):
    return {"aggregate": ["D"]}


builder = StateGraph(MyState)
builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_b2)
builder.add_node(node_d)

builder.set_entry_point("node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_a", "node_c")
builder.add_edge("node_c", "node_d")
builder.add_edge("node_b", "node_b2")
builder.add_edge("node_b2", "node_d")
builder.add_edge("node_d", END)

graph = builder.compile()
# result=graph.invoke({})
# print(result)

print("获取图的节点")
print(graph.nodes)
print("获取图的通道")
print(graph.channels)

# 获取某个节点的订阅和写入
print("获取某个节点的订阅和写入")
print("订阅")
print(graph.nodes["node_a"].triggers)
print("写入")
print(graph.nodes["node_a"].writers)
