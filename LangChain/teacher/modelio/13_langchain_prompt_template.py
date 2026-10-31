"""

"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = init_chat_model("openai:qwen-flash")

# template = PromptTemplate.from_template("给我将一个关于{topic}的笑话")
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{role},你的回答永远少于100字"),
    ("user", "给我将一个关于{topic}的笑话")
])

data = {
    "role": "冷笑话师傅",
    "topic": "狗"
}
china1 = template | llm
china2 = template | llm | StrOutputParser()
result1 = china1.invoke(data)
result2 = china2.invoke(data)
print(type(result1))  # <class 'langchain_core.messages.ai.AIMessage'>
print(result1)
print(type(result2))  # <class 'langchain_core.messages.base.TextAccessor'>
print(result2)
