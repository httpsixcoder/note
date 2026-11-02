"""
    测试:Reduces函数
"""
import operator

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated


def test_reducer(left, right):
    return left + right


class MyState(TypedDict):
    # key: Annotated[list[str], test_reducer]
    key: Annotated[list[str], operator.add]


def test_node(state: MyState):
    return {"key": ["world"]}


builder = StateGraph(MyState)

builder.add_node(test_node)

builder.add_edge(START, "test_node")
builder.add_edge("test_node", END)

graph = builder.compile()

result = graph.invoke({"key": ["hello"]})
print(result)
