""""
    测试： 节点的输入，节点函数可以使用的参数
"""
from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime


class Test():
    def invoke(self):
        print("hi, this is invoke")


class MyState(TypedDict):
    key: str


def test_node(state: TypedDict, config: RunnableConfig, runtime: Runtime):
    print("状态管理", state)
    # 获取执行图对象时设置的config参数的值
    print("传参数", config["configurable"]["test_config"])
    # 获取执行图对象时设置的context参数的值
    print("runtime", runtime.context["test"].invoke())
    return {"key": "value"}


builder = StateGraph(MyState)
builder.add_node(test_node)
builder.set_entry_point("test_node")

graph = builder.compile()

context = {
    "test": Test()
}

result = graph.invoke(
    input={},
    config={
        "configurable": {
            "test_config": "what fuck tis"
        }
    },
    context=context
)
print(result)
