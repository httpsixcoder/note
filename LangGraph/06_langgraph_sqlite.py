"""
    测试：使用Sqlite实现长期记忆
        1.创建sqlite的连接对象和检查点对象
        conn = sqlite3.connect(
            "./database.db",
            check_same_thread=False
        )
        checkpointer = SqliteSaver(conn)
        2.再图对象编译时设置checkpointer
        graph = builder.compile(checkpointer=checkpointer)
        3.在执行图对象时设置config
        # 第一次执行
        # result = graph.invoke({}, config={"configurable": {"thread_id": "abc123"}})
        # 第二次执行，必须输入None，才可以实现断点续传
        result = graph.invoke(None, config={"configurable": {"thread_id": "abc123"}})
"""
import sqlite3
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import START
from langgraph.graph import StateGraph

# 创建sqlite连接对象
conn = sqlite3.connect(
    "./database.db",
    check_same_thread=False
)
# 创建检查点对象
checkpointer = SqliteSaver(conn)


# 创建状态类
class MyState(TypedDict):
    key1: str
    key2: str
    key3: str


# 创建节点
def node1(state: MyState):
    print(f"第一个节点：{state}")
    return {"key1": "节点1"}


def node2(state: MyState):
    # 第一次执行后注释
    # raise Exception("node2节点出现故障")
    print(f"第二个节点：{state}")
    return {"key2": "节点222"}


def node3(state: MyState):
    print(f"第三个节点：{state}")
    return {"key3": "节点333333333"}


# 创建StateGraph对象
builder = StateGraph(MyState)
# 添加节点和边
builder.add_node(node1)
builder.add_node(node2)
builder.add_node(node3)
builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", "node3")

# 编译得到图对象
graph = builder.compile(checkpointer=checkpointer)

# 执行图对象
# 第一次执行
# result = graph.invoke({}, config={"configurable": {"thread_id": "abc123"}})
# 第二次执行，必须输入None，才可以实现断点续传
result = graph.invoke(None, config={"configurable": {"thread_id": "abc123"}})
print(result)
