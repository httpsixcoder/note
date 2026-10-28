"""
    测试：通过LangChain调用大模型
    方式1：
        使用ChatOpenAI()
        创建模型对象
        创建模型对象时，自动读取环境变量中的OPENAI_API_KEY和OPENAI_BASH_URL所对应的值，
        分别为api_key和base_url参数赋值
    方式2：
        使用init_chat_model()
        创建模型对象
        此函数中必须把配置model_provider，指定模型的提供者
        api_key和base_url也可以自动读取环境变量中的OPENAI_API_KEY和OPENAI_BASH_URL
"""
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

# 1.读取.env
load_dotenv()
# 2.创建大模型对象
# llm = ChatOpenAI(
#     model="qwen-flash",
#     # 可以省略
#     # api_key=os.getenv("OPENAI_API_KEY"),
#     # base_url=os.getenv("OPENAI_BASH_URL"),
# )
llm = init_chat_model(
    model="qwen-flash",
    model_provider="openai"
)

# 3.调用大模型
result = llm.invoke([{"role": "user", "content": "给我讲个笑话"}])
print(result.content)
