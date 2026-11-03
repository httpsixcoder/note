"""
    测试：LangGraph中的条件边
"""
from typing import TypedDict

from langgraph.graph import StateGraph


class MyState(TypedDict):
    value: int
    step: str


def node_a(state: MyState):
    print("node_a")
    return {"step": "ndoe_a"}


def node_b(state: MyState):
    print("node_b")
    return {"value": state["value"] * 2, "step": "node_b"}


def node_c(state: MyState):
    print("node_c")
    return {"value": state["value"] + 100, "step": "node_c"}


# 条件边的路由函数，参数是状态类对象，返回的结果是指向节点的名称或者别名
def condition_router(state: MyState):
    if state["value"] % 2 == 0:
        return "b"
    else:
        return "c"
    print("condition_router")


builder = StateGraph(MyState)

builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)

builder.set_entry_point("node_a")
builder.add_conditional_edges(
    source="node_a",
    path=condition_router,
    path_map={
        "b": "node_b",
        "c": "node_c",
    }
)

graph = builder.compile()
result = graph.invoke({"value": 7})
print(result)
