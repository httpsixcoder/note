"""
    调用大模型有三种方式：直接调用，流式调用，批次调用
    每一种调用方式又分为同步和异步的方式
    1.invoke() 和 ainvoke()
    2.stream() 和 astream()
    3.batch() 和 abatch()
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv()

llm = init_chat_model(
    "openai:qwen-flash"
)
results = llm.batch([
    [HumanMessage("你好")],
    [HumanMessage("什么是LangChain")]
])
# print(results) # 列表 List

for result in results:
    print(result.content)
    print("*"*100)
