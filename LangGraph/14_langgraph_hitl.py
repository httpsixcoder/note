"""
    测试：人工审核
"""
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command


class MyState(TypedDict):
    recipient: str
    amount: int
    memo: str
    approved: bool
    final_status: str


def review_transfer(state: MyState):
    # 获取当前的咋转账信息
    pending_transfer = {
        "recipient": state["recipient"],
        "amount": state["amount"],
        "memo": state["memo"],
    }
    # 使用interrupt()函数进行中断,实现人工审核,且返回值为人工审核的结果
    interrupt_result = interrupt({
        "title": "转账审核",
        "pending_transfer": pending_transfer,
        "instruction": "请返回 bool(是否批准) 或 dict(可改 recipient/amount/memo，并带 approved 字段)。",
    })
    # 创建存储修改之后的转账信息的字典
    updated_transfer = pending_transfer
    # 存储最终批准或者拒绝的变量
    approved = False
    if isinstance(interrupt_result, bool):
        approved = interrupt_result
    elif isinstance(interrupt_result, dict):
        approved = interrupt_result.get("approve", True)
        for key in updated_transfer.keys():
            if key in interrupt_result.keys():
                updated_transfer[key] = interrupt_result[key]
    return {
        "recipient": updated_transfer["recipient"],
        "amount": updated_transfer["amount"],
        "memo": updated_transfer["memo"],
        "approved": approved,
    }
    # print(interrupt_result)


def execute_transfer(state: MyState):
    if not state["approved"]:
        return {"final_status": "拒绝转账"}
    return {f"final_status": f"批准转账，{state=}"}


checkpointer = InMemorySaver()

# 创建StateGraph对象
builder = StateGraph(MyState)

builder.add_node(review_transfer)
builder.add_node(execute_transfer)

builder.set_entry_point("review_transfer")
builder.add_edge("review_transfer", "execute_transfer")

# 编译得到图对象
graph = builder.compile(checkpointer=checkpointer)

# 人工审核必须结合记忆功能实现
config = {
    "configurable": {
        "thread_id": "abc"
    }
}
result = graph.invoke(
    input={
        "recipient": "张三",
        "amount": "10",
        "memo": "午饭AA",
    },
    config=config
)

if "__interrupt__" in result:
    # 获取人工审核信息
    interrupt_msg = result["__interrupt__"][0].value
    print(f"节点执行过程中进行可人工审核，审核信息：{interrupt_msg}")
    # 设置人工审核的结果
    # interrupt_result = True  # 审核通过
    # interrupt_result=False # 审核不通过
    interrupt_result={
        "recipient": "李四",
        "amount": "1000",
        "memo": "晚饭请客",
        "approved": True,
    } # 审核通过，但是修改转账信息

    # 第二次执行图对象，返回人工审核的结果
    result = graph.invoke(
        input=Command(resume=interrupt_msg),
        config=config
    )
    print(result)
print(result)
