from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm=init_chat_model(
    "openai:qwen-flash"
)
result=llm.invoke([
    SystemMessage("要求输出json格式，其中包含prime信息，表示素有素数，数组格式；包含count信息，表示素数的数量，数值类型"),
    HumanMessage("帮我查询1-500之间所有的素数以及素数的数量")
])

print(result.content)