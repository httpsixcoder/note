"""
    测试： 同时使用大模型对象，提示词模板，格式化输出
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

data = {
    "topic": "生活"
}

template = ChatPromptTemplate.from_messages([
    ("user", "给我讲一个关于{topic}的正常小笑话，爆笑的！！！")
])
# prompt = template.invoke(data)

llm = init_chat_model("openai:qwen-flash")
# result = llm.invoke(prompt)

# parser = StrOutputParser()
# str_result = parser.invoke(result)

chain = template | llm | StrOutputParser()
str_result = chain.invoke(data)
print(str_result)
