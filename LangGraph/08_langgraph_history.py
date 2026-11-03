"""
    测试：获取图对象的节点、通道、节点的订阅和写入
"""
import operator
import sqlite3
from typing import TypedDict, Annotated, List

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import END
from langgraph.graph import StateGraph

coon = sqlite3.connect(
    "./test.db",
    check_same_thread=False
)
checkPointer = SqliteSaver(coon)


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

graph = builder.compile(checkpointer=checkPointer)

config = {
    "configurable": {
        "thread_id": "xyz"
    }
}
result = graph.invoke({}, config)
# print(result)

# 方法1
# 获取 graph.get_state()获取最近的一次历史状态
# print(graph.get_state(config))
# StateSnapshot 状态快照
# StateSnapshot(values={'aggregate': ['A', 'B', 'C', 'B2', 'D', 'D', 'A', 'B', 'C', 'B2', 'D', 'D']}, next=(), config={'configurable': {'thread_id': 'xyz', 'checkpoint_ns': '', 'checkpoint_id': '1f1d72c6-c22d-6cc9-800a-c665643bd19b'}}, metadata={'source': 'loop', 'step': 10, 'parents': {}}, created_at='2026-11-03T02:15:21.795296+00:00', parent_config={'configurable': {'thread_id': 'xyz', 'checkpoint_ns': '', 'checkpoint_id': '1f1d72c6-c22d-6cc8-8009-ba1d900737ab'}}, tasks=(), interrupts=())

# 方法2
# 获取图对象执行过程中所有的历史状态
history_list = graph.get_state_history(config)
for item in history_list:
    print(item)
