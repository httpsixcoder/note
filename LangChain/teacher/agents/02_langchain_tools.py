"""
    测试：使用LangChain（非智能体）调用工具
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()


# 创建工具所对应的函数
# 方式1：
@tool(description="获取某个城市某天的天气情况")
def get_weather(city, date):
    return f"{city}的{date}天气是多云转晴"


# 方式2：
# def get_weather(city, date):
#     """获取某个城市某天的天气情况"""
#     return f"{city}的{date}天气是多云转晴"


# llm
llm = init_chat_model("openai:qwen-flash")
# llm绑定工具
llm = llm.bind_tools([get_weather])

# 设置提示词
messages = [
    # ("role", "user", "content", "北京2025-12-21的天气怎么样")
    # {"role": "user", "content": "北京2025-12-21的天气怎么样"}
    HumanMessage("北京2025-12-21的天气怎么样")

]
# 第一次调用大模型
result1 = llm.invoke(messages)

# 将第一次大模型调用的结果存储到消息列表中messages
messages.append(result1)

# 调用工具
tool_call = result1.tool_calls[0]
args = tool_call.get("args")
weather = get_weather.invoke(args)
# 将工具调用的结果存储到消息列表中messages
messages.append(
    ToolMessage(
        content=weather,
        tool_call_id=tool_call.get("id")
    )
)

# 第二次调用大模型
result2 = llm.invoke(messages)

print(result2.content)
