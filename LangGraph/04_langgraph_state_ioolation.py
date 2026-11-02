"""
    测试：LangGraph当中节点所接收的是非全局的状态,状态数据隔离,节点间的geli
"""

from typing import TypedDict

from langgraph.constants import END
from langgraph.graph import StateGraph


# 1.创建状态类
class MyState(TypedDict):
    query: str
    final_answer: str


# 创建非全局的私有状态
class ResultState(TypedDict):
    query: str
    rag_result: str
    web_result: str


# 2.创建节点，节点的本质是函数
def rag_node(state: MyState):
    print(f"rag_node:{state}")
    return {"rag_result": "这是RAG检索的结果"}


def web_node(state: MyState):
    print(f"web_node:{state}")
    return {"web_result": "这是Web查询的结果"}


def final_node(state: ResultState):
    print(f"final_answer:{state}")
    return {
        "final_answer": f" query:{state["query"]},rag_result:{state['rag_result']}, web_result:{state['web_result']}"}


# 3.创建StateGraph对象
builder = StateGraph(state_schema=MyState)

# 4.添加节点
builder.add_node(rag_node)
builder.add_node(web_node)
builder.add_node(final_node)
# 4.使用节点的名称添加边

builder.set_entry_point("rag_node")
builder.set_entry_point("web_node")
builder.add_edge("rag_node", "final_node")
builder.add_edge("web_node", "final_node")
builder.add_edge("final_node", END)

# 5.编译StateGraph得到图对象
graph = builder.compile()

# 6.执行图对象
result = graph.invoke({"query": "测试langGraph"})
print(result)
