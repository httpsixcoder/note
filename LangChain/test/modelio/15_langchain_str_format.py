"""
    测试：StrOutputParser()
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
# 创建模型对象
llm=init_chat_model("openai:qwen-flash")

# 调用模型
result=llm.invoke("给我讲一个笑话")

# 创建格式化对象
parser=StrOutputParser()

# 对模型结果进行格式化
str_result=parser.invoke(result)

print(str_result)