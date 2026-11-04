"""
    测试：LangGraph入门案例【改进】
"""
import operator
from typing import TypedDict, List, Annotated

from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph


class MyState(TypedDict):
    count: Annotated[List[str], operator.add]
    query: str
    rag_result: str
    web_result: str
    final_answer: str


class InputSchema(TypedDict):
    query: str


class OutputSchema(TypedDict):
    final_answer: str


# 2.创建节点，节点的本质是函数
def rag_node(state: MyState) -> dict[str, str]:
    return {"rag_result": "这是RAG检索的结果", "count": ["rag_node"]}


def web_node(state: MyState) -> dict[str, str]:
    state["count"] = "web_node"
    return {"web_result": "这是Web查询的结果", "count": ["web_node"]}


def final_node(state: MyState) -> dict[str, str]:
    answer = (
        f"count:{state['count']};"
        f"query:{state['query']}, "
        f"rag_result:{state['rag_result']}, "
        f"web_result:{state['web_result']}"
    )
    return {"final_answer": answer}


def compile_graph() -> CompiledStateGraph:
    builder = StateGraph(
        state_schema=MyState,
        input_schema=InputSchema,
        output_schema=OutputSchema,
    )

    builder.add_node("rag", rag_node)
    builder.add_node("web", web_node)
    builder.add_node("final", final_node)

    builder.add_edge(START, "rag")
    builder.add_edge(START, "web")
    builder.add_edge("rag", "final")
    builder.add_edge("web", "final")
    builder.add_edge("final", END)

    return builder.compile()


if __name__ == "__main__":
    graph = compile_graph()
    result = graph.invoke({"query": "测试langGraph"})
    print(result)
    # print(graph.get_graph().draw_ascii())  # 有返回值
    # graph.get_graph().print_ascii()
