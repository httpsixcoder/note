from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = init_chat_model("openai:qwen-flash")

chain_1 = ChatPromptTemplate.from_messages(
    [("user", "分析这首诗{poem}，做鉴赏,浓缩成少于200个字")]) | llm | StrOutputParser()
chain_2 = ChatPromptTemplate.from_messages(
    [("user", "分析这首诗{poem}，做分析,浓缩成少于200个字")]) | llm | StrOutputParser()

chain_all = ChatPromptTemplate.from_messages(
    ["user", "分析这两个鉴赏，第一个：{chain_poem1},第二个{chain_poem2},哪个更好，为什么，浓缩成少于200个字"]) | llm | StrOutputParser()

main_chain = RunnableParallel(chain_poem1=chain_1, chain_poem2=chain_2) | chain_all

poem = """
追风赶月莫停留，
平芜尽处是春山。
"""

result = main_chain.invoke({"poem": poem})
print(result)
