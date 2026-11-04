"""
    测试：验证异步 checkpointer
"""
import asyncio
from pathlib import Path
from typing import TypedDict

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph


class MyState(TypedDict):
    key1: str
    key2: str


def node1(state: MyState) -> dict[str, str]:
    print(f"node1：{state}")
    return {"key1": "value1"}


def node2(state: MyState) -> dict[str, str]:
    # raise Exception("node2")
    print(f"node2：{state}")
    return {"key2": "value2"}


def compile_graph(checkpointer: AsyncSqliteSaver) -> CompiledStateGraph:
    builder = StateGraph(MyState)

    builder.add_node("node1", node1)
    builder.add_node("node2", node2)

    builder.add_edge(START, "node1")
    builder.add_edge("node1", "node2")
    builder.add_edge("node2", END)

    return builder.compile(checkpointer=checkpointer)


async def main() -> None:
    # 字符串转成 Path 对象，再转成绝对路径，最后转回字符串
    db_path = str(Path("./database.db").resolve())
    config = {"configurable": {"thread_id": "async_checkpointer_test"}}

    # 异步类方法，根据路径创建一个异步连接并返回 AsyncSqliteSaver 实例的异步上下文管理器，checkpointer：检查点器实例。
    async with AsyncSqliteSaver.from_conn_string(db_path) as checkpointer:
        graph = compile_graph(checkpointer)

        # aget_state(config)：根据 config（含 thread_id）查询该会话的最新检查点状态。
        snapshot = await graph.aget_state(config)

        if snapshot.values:
            print(f"发现检查点，从该状态恢复: {snapshot.values}")
            result = await graph.ainvoke(input=None, config=config)
        else:
            print("无检查点，全新执行")
            result = await graph.ainvoke(input={}, config=config)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
