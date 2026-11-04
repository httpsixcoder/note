"""
    测试：LangGraph当中节点所接收的是非全局的状态,状态数据隔离,节点间的隔离
"""

from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph


class MyState(TypedDict):
    query: str
    rag_result: str
    web_result: str
    final_answer: str


class ResultState(TypedDict):
    query: str
    rag_result: str
    web_result: str


def rag_node(state: MyState) -> dict[str, str]:
    print(f"rag_node:{state}")
    return {"rag_result": "这是RAG检索的结果"}


def web_node(state: MyState) -> dict[str, str]:
    print(f"web_node:{state}")
    return {"web_result": "这是Web查询的结果"}


def final_node(state: ResultState) -> dict[str, str]:
    print(f"final_node:{state}")
    answer = (
        f"query:{state['query']}, "
        f"rag_result:{state['rag_result']}, "
        f"web_result:{state['web_result']}"
    )
    return {"final_answer": answer}


def build_graph() -> CompiledStateGraph:
    builder = StateGraph(state_schema=MyState)

    builder.add_node("rag", rag_node)
    builder.add_node("web", web_node)
    # ✅ 关键：用 input_schema 限制 final 节点可见的字段
    builder.add_node("final", final_node, input_schema=ResultState)

    # 并行 fan-out：必须用 add_edge(START, ...) 两次
    builder.add_edge(START, "rag")
    builder.add_edge(START, "web")

    builder.add_edge("rag", "final")
    builder.add_edge("web", "final")
    builder.add_edge("final", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"query": "测试langGraph"})
    print(result)
