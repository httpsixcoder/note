"""
    LCEL 链式调用
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm=init_chat_model("openai:qwen-flash")

prompt_template=ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的评论员"),
    ("user", "请评价{product}的优缺点, 包括{aspect1}和{aspect2}.")
])
# 底层构建了一个 RunnableSequence（可运行序列）对象。
chain=prompt_template | llm

data={
    "product": "拯救者Y9000P",
    "aspect1": "性能",
    "aspect2": "性价比"
}
result=chain.invoke(data)
print(result.content)