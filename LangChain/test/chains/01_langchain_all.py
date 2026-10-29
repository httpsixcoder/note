from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# template
prompt_template = ChatPromptTemplate.from_template("将{text}翻译为英文")
# prompt
prompt=prompt_template.invoke({"text":"再见"})

# llm
llm=init_chat_model("openai:qwen-flash")
# 调用
result=llm.invoke(prompt)

# 格式化输出
parser=StrOutputParser()
str_result=parser.invoke(result)
print(str_result)