"""
    测试：获取图对象的节点、通道、节点的订阅和写入
    节点 = 用户函数 + 订阅哪些通道 + 完成后往哪些通道写（编译后是 PregelNode 包装对象）
    边 = builder 阶段声明的节点间传递关系
    通道 = 承载信息的邮箱，分两类：状态通道（State 字段，存数据）和触发通道（branch:to:X，传控制信号）。边编译后消失，融化为一对读写关系
    订阅（triggers） = 哪些通道的更新会唤起我（输入侧）
    写入（writers） = 我完成后向哪些通道发更新（输出侧，控制流和数据流都走这里）
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
