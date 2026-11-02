"""
    # 创建输入结构的状态类
    class InputSchema(TypedDict):
        query: str
    # 创建输出结构的状态类
    class OutputSchema(TypedDict):
        final_answer: str

    测试：输入输出隔离
    创建StateGraph对象时,可以设置三个参数
    state_schema:设置状态类的结构
    input_schema:图对象执行时,只能为某些属性赋初始值
    output_schema:图对象执行后,只能输出某些属性的值
"""

from typing import TypedDict

from langgraph.constants import END
from langgraph.graph import StateGraph


# 1.创建状态类
class MyState(TypedDict):
    query: str
    test: str
    rag_result: str
    web_result: str
    final_answer: str


# 创建输入结构的状态类
class InputSchema(TypedDict):
    query: str


# 创建输出结构的状态类
class OutputSchema(TypedDict):
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
builder = StateGraph(state_schema=MyState, input_schema=InputSchema, output_schema=OutputSchema)

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
result = graph.invoke({"query": "测试langGraph", "test": "hello"})
print(result)
