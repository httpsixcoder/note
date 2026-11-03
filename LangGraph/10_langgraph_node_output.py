"""
    测试：LangGraph节点的输出
"""
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class MyState(TypedDict):
    query: str
    rag_result: str
    web_result: str
    final_answer: str


def rag_node(state: MyState):
    print(f"rag_node:{state}")
    state["rag_result"] = "这是RAG检索的结果"
    return state


def web_node(state: MyState):
    print(f"web_node:{state}")
    state["web_result"] = "这是Web查询的结果"
    return state


def final_node(state: MyState):
    print(f"final_answer:{state}")
    state[
        "final_answer"] = f" query:{state["query"]},rag_result:{state['rag_result']}, web_result:{state['web_result']}"
    return state


# 3.创建StateGraph对象
builder = StateGraph(MyState)

# 4.添加节点
builder.add_node(rag_node)
builder.add_node(web_node)
builder.add_node(final_node)

# 并行报错 每一个超步中query只能接收一个值，
# builder.set_entry_point("rag_node")
# builder.set_entry_point("web_node")
# builder.add_edge("rag_node", "final_node")
# builder.add_edge("web_node", "final_node")
# builder.add_edge("final_node", END)
# 串行没问题
builder.set_entry_point("rag_node")
builder.add_edge("rag_node", "web_node")
builder.add_edge("web_node", "final_node")

graph = builder.compile()

result = graph.invoke({"query": "测试langGraph"})
print(result)
# graph.get_graph().print_ascii()  # 没有返回值，直接打印
