"""
    测试：创建状态类的两种方式
        1.继承TypedDict
        2.继承BaseModel
        区别:
        1.继承BaseModel的状态类具有校验功能,在创建对象时候,每个属性都必须有初始值,或者默认值
        2.继承TypedDict的状态类可以以自带你的方式访问对象中的属性,
        但是继承BaseModel的状态类只能以对象.属性的方式访问状态类中的属性
"""

from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel


# 1.创建状态类
# class MyState(TypedDict):
# 继承BaseModel的状态类,要校验功能,必须设置默认值
class MyState(BaseModel):
    query: str = None
    rag_result: str = None
    web_result: str = None
    final_answer: str = None


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
        # 如果用继承TypedDict的状态管理是可以用字典的方式访问
        # "final_answer": f" query:{state["query"]},rag_result:{state['rag_result']}, web_result:{state['web_result']}"}
        # 如果用继承BaseModel的状态管理是用state.query,来访问
        "final_answer": f" query:{state.query},rag_result:{state.rag_result}, web_result:{state.web_result}"}


# 3.创建StateGraph对象
builder = StateGraph(MyState)

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
