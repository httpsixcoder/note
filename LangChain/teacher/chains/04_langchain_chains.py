from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

load_dotenv()
llm = init_chat_model("openai:qwen-flash")

chain1 = ChatPromptTemplate.from_template("对这首诗{poem}做一下赏析，分析含义") | llm | StrOutputParser()
chain2 = ChatPromptTemplate.from_template("对这首诗{poem}做一下赏析，分析意境") | llm | StrOutputParser()

chain3 = ChatPromptTemplate.from_template(
    "对这两个赏析：第一个{result1}，第二个{result2}，进行总结") | llm | StrOutputParser()

# 有黄线错误，解决：# type: ignore

# chain = {"result1": chain1, "result2": chain2} | chain3 # type: ignore
chain = RunnableParallel(result1=chain1, result2=chain2) | chain3

data = """
莫听穿林打叶声，
何妨吟啸且前行。
"""

result = chain.invoke({"poem": data})
print(result)
