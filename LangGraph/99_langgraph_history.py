"""

"""
import operator
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import TypedDict, Annotated

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph


class MyState(TypedDict):
    value: Annotated[list[str], operator.add]


def node_a(state: MyState) -> dict[str, list[str]]:
    return {"value": ["aaa"]}


def node_b(state: MyState) -> dict[str, list[str]]:
    return {"value": ["bbb"]}


def node_c(state: MyState) -> dict[str, list[str]]:
    return {"value": ["ccc"]}


def node_b2(state: MyState) -> dict[str, list[str]]:
    return {"value": ["b2b2b2b2"]}


def node_d(state: MyState) -> dict[str, list[str]]:
    return {"value": ["ddd"]}


def compiled_graph(checkpointer: SqliteSaver) -> CompiledStateGraph:
    builder = StateGraph(MyState)

    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_node("c", node_c)
    builder.add_node("b2", node_b2)
    builder.add_node("d", node_d)

    builder.add_edge(START, "a")
    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_edge("b", "b2")
    # 等待c和b2都执行完，在执行d
    # builder.add_edge(["c", "b2"], "d")
    # 并行
    builder.add_edge("b2", "d")
    builder.add_edge("c", "d")
    builder.add_edge("d", END)

    return builder.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    db_path = str(Path("./test.db").resolve())
    config = {"configurable": {"thread_id": "xyz-1"}}

    # 默认 check_same_thread=False，
    with SqliteSaver.from_conn_string(db_path) as saver:
        graph = compiled_graph(saver)
        result = graph.invoke({}, config=config)
        print(f"最终结果{result}")

        snapshot = graph.get_state(config=config)
        print(f"最近状态: {snapshot.values}")

        for item in graph.get_state_history(config=config):
            print(f"step={item.metadata.get('step')}, values={item.values}")
