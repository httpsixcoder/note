"""
    测试：调用ollama
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from openai import base_url

load_dotenv()

llm = init_chat_model(
    # 需要配置本地ollama的设置
    # "ollama:qwen3:8b",
    "ollama:deepseek-r1:7b",
    # 默认可以不写隐式获取，，如果端口号改变则需要显式写出【ollama端口号11434】
    # base_url="http://localhost:11434",

)
result = llm.invoke([
    HumanMessage("你好")
])
print(result.content)
