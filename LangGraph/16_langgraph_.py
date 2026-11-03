"""
    测试：LangGraph实现可控循环
"""
from typing import TypedDict

from langgraph.constants import END
from langgraph.graph import StateGraph


class MyState(TypedDict):
    count: int
    result: str
    max_count: int


def node_a(state: MyState) -> dict:
    print("node_a", state["count"])
    return {
        "count": state["count"] + 1,
        "result": f"已经完成处理了{state['count']}次循环",
    }


def node_b(state: MyState) -> dict:
    return {
        "result": "辅助处理",
    }


def condition_router(state: MyState):
    if state["count"] > state["max_count"]:
        return END
    else:
        return "node_b"


builder = StateGraph(MyState)

builder.add_node(node_a)
builder.add_node(node_b)

builder.set_entry_point("node_a")
builder.add_conditional_edges(
    "node_a",
    condition_router,
)
builder.add_edge("node_b", "node_a")

graph = builder.compile()
# config={"recursion_limit": 3} 设置最大的循环次数
result = graph.invoke({"count": 0, "max_count": 3}, config={"recursion_limit": 10})
print(result)
