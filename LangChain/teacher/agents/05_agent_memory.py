"""
    测试：智能体实现短期记忆
    实现步骤：
        1.创建检查点对象
        2.创建智能体时，为checkpointer参数赋值
"""
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
llm = init_chat_model("openai:qwen-flash")
# 创建检查点对象
checkpointer = InMemorySaver()
agent = create_agent(model=llm, checkpointer=checkpointer)

# 第一次调用agent
result1 = agent.invoke(
    input={
        "messages": [
            ("user", "你好我是小明")
        ]
    },
    config={
        "configurable": {
            "thread_id": "abc"
        }
    }
)
print(result1["messages"][-1])

# 第二次调用智能体
result2 = agent.invoke(
    input={
        "messages": [
            ("user", "你好,我是谁")
        ]
    },
    config={
        "configurable": {
            "thread_id": "abc"
        }
    }
)
print(result2["messages"][-1])
print("===========================")
print(result1)
print(result2)
