import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = init_chat_model(
    "openai:qwen-flash",     # "provider:model" 写法最省事
    temperature=0.2,           # 抽取/分类用 0~0.3；创意写作才调高
    timeout=30,                # 秒，必须有，否则挂死
    max_retries=2,             # 网络层重试（≠ Agent 中间件的模型重试）
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)
resp = llm.invoke([
    SystemMessage("你是严谨的技术文档助手，不确定就说不确定。"),
    HumanMessage("LangChain 的 checkpoint 是什么？"),
])
print(resp.content)                 # 纯文本（最常用）
print(resp.usage_metadata)          # {'input_tokens':..,'output_tokens':..,'total_tokens':..}
print(resp.tool_calls)              # [{'name':'..','args':{..},'id':'..'}] 仅当调工具