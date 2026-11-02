"""
    测试：LangGraph入门案例
    LangGraph步骤：
        1.创建状态类,需要基础TypedDict，对象可以以字典的方式访问
        2.创建节点，节点的本质是函数
            节点函数至少由一个状态类类型的参数（最多三个参数），
            在各个节点之间传递数据，或者共享数据
            以方便上一个节点将最终的结果传递到当前的节点中
            节点函数的返回值是一个字典，一帮用于更新状态对象中的属性的
        3.创建StateGraph对象
        4.添加节点和边
        5.编译StateGraph对象得到图对象
        6.执行图对象
"""
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1.创建状态类
class MyState(TypedDict):
    query: str
    rag_result: str
    web_result: str
    final_answer: str


# 2.创建节点，节点的本质是函数
def rag_node(state: MyState):
    print(f"rag_node:{state}")
    return {"rag_result": "这是RAG检索的结果"}


def web_node(state: MyState):
    print(f"web_node:{state}")
    return {"web_result": "这是Web查询的结果"}


def final_node(state: MyState):
    print(f"final_answer:{state}")
    return {
        "final_answer": f" query:{state["query"]},rag_result:{state['rag_result']}, web_result:{state['web_result']}"}


# 3.创建StateGraph对象
builder = StateGraph(MyState)

# 4.添加节点
builder.add_node(rag_node)
builder.add_node(web_node)
builder.add_node(final_node)
# 4.使用节点的名称添加边
# 若添加节点的时候未指定节点名，则节点的名称和函数名一致，builder.add_node(rag_node)-->rag_node
# 若添加节点的时候指定节点名，则节点的名称由指定的为准，builder.add_node("rag",rag_node)-->rag
# START和END是LangGraph提供的虚拟节点，开始节点START必须设置，而END可选
# 设置开始节点的两种方式：
#   1.builder.add_edge(START, "rag_node")
#   2.builder.set_entry_point("rag_node")

# builder.add_edge(START, "rag_node")
# builder.add_edge(START, "web_node")
builder.set_entry_point("rag_node")
builder.set_entry_point("web_node")
builder.add_edge("rag_node", "final_node")
builder.add_edge("web_node", "final_node")
builder.add_edge("final_node", END)

# 5.编译StateGraph得到图对象
graph = builder.compile()

# 6.执行图对象
# 其中的input参数设置初始状态
result = graph.invoke({"query": "测试langGraph"})
# print(result)

# print(graph.get_graph().draw_ascii())  # 有返回值
graph.get_graph().print_ascii()  # 没有返回值，直接打印
