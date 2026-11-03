"""

"""
import sqlite3
from typing import TypedDict


from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

# 创建sqliter连接对象
connection = sqlite3.connect(
    "./test1.db",  # 表示sqlite存储数据的文件的位置
    check_same_thread=False,  # 表示不同的线程可以访问存储数据的文件
)
# 创建检查点对象
checkpointer = SqliteSaver(connection)


# 创建状态类
class MyState(TypedDict):
    key1: str
    key2: str
    key3: str


# 创建节点
def node1(state: MyState):
    print(f"node1:{state}")
    return {"key1": "value1"}


def node2(state: MyState):
    # raise Exception("node2出错")
    print(f"node2:{state}")
    return {"key2": "value2"}


def node3(state: MyState):
    print(f"node3:{state}")
    return {"key3": "value3"}


builder = StateGraph(MyState)

builder.add_node(node1)
builder.add_node(node2)
builder.add_node(node3)
builder.set_entry_point("node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", "node3")

graph = builder.compile(checkpointer= checkpointer)

# result = graph.invoke({}, config={"configurable": {"thread_id": "123"}})
result = graph.invoke(None, config={"configurable": {"thread_id": "123"}})
print(result)
