from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = init_chat_model("openai:qwen-flash")

chain1 = ChatPromptTemplate.from_template("把这个句子{text}翻译成英文") | llm | StrOutputParser()
chain2 = ChatPromptTemplate.from_template("把这个句子{text}翻译成韩文") | llm | StrOutputParser()
chain3 = ChatPromptTemplate.from_template("把这个句子{text}翻译成俄文") | llm | StrOutputParser()

chain_all = RunnableParallel(chain1=chain1, chain2=chain2, chain3=chain3)
results = chain_all.invoke({"text": "我很开心"})
print(results)
print(type(results))
print(results["chain1"])
print(results["chain2"])
print(results["chain3"])
