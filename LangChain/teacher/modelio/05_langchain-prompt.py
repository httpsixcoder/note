"""
    测试： LangChain调用模型时候，设置提示词的方式：
    1.直接使用字符串设置提示词
    3.使用列表 + 字典的方式设置提示词
     {
         "role": "system",
         "content": "系统提示词"
     },
     {
         "role": "user",
         "content": "用户提示词"
     }
    3.使用列表 + 元组的方式设置提示词
        ("system", "系统提示词"),
        ("user", "用户提示词")
    4.使用消息对象设置提示词
    [
        SystemMessage("系统提示词"),
        HumanMessage("用户提示词")
    ]
    LangChain中提供的消息对象：
    a> SystemMessage
    b> HumanMessage
    c> AIMessage
    d> ToolMessage
"""
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(
    model="qwen-flash"
)
# 方式1：
# result=llm.invoke("你是谁")
# 方式2：
# result = llm.invoke([
#     {
#         "role": "system",
#         "content": "系统提示词"
#     },
#     {
#         "role": "user",
#         "content": "什么是LangChain"
#     }
# ])
# 方式3：
# result = llm.invoke([
#     ("system", "你是一个专业的冷笑话高手"),
#     ("user", "你说一个冷笑话")
# ])
# 方式4：
result = llm.invoke([
    SystemMessage("你是一个专业的法律顾问"),
    HumanMessage("吃饭不给钱触犯了什么法律")
])
print(result.content)
