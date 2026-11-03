"""
    测试：节点的重试功能
    不会进行重试的异常：
    ValueError, TypeError, ArithmeticError, ImportError
    LookupError, NameError, SyntaxError, RuntimeError
    ReferenceError, StopIteration, StopAsyncIteration, OSError
    # 添加节点和边
    builder.add_node(test_node, retry_policy=RetryPolicy(max_attempts=5))
"""
from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy


class MyState(TypedDict):
    result: str


# 记录重试次数
attempt_count = 0


def test_node(state: MyState):
    global attempt_count
    attempt_count += 1
    print(f"当前第{attempt_count}次执行")
    if attempt_count < 3:
        # raise NameError("运行异常") # 无法节点重试
        raise Exception("运行异常")
    else:
        return {"result": f"第{attempt_count}次执行节点"}


builder = StateGraph(MyState)
builder.add_node(test_node, retry_policy=RetryPolicy(max_attempts=5))
builder.set_entry_point("test_node")
graph = builder.compile()

result = graph.invoke({})
print(result)
