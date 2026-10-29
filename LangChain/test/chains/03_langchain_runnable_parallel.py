from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm=init_chat_model("openai:qwen-flash")

en_chain=ChatPromptTemplate.from_messages([("user","把这个句子{text}翻译成英文")])|llm|StrOutputParser()
ok_chain=ChatPromptTemplate.from_messages([("user","把这个句子{text}翻译成韩文")])|llm|StrOutputParser()

# chains=RunnableParallel(en_chain=en_chain,ok_chain=ok_chain)
# result=chains.invoke({"text":"你好呀"})
result=RunnableParallel(en_chain=en_chain,ok_chain=ok_chain).invoke({"text":"今天天气真好"})
print(result)