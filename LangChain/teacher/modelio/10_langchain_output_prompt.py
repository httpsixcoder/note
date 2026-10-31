"""
    测试：通过提示词约束模型输出
"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from openai import BaseModel
from pydantic import Field

load_dotenv()

llm = init_chat_model("openai:qwen-flash")


# result = llm.invoke([
#     ("user",
#      "输出100之间所有素数，以json的格式输出，其中包含键prime，数组类型，表示所有素数；包含count，数值类型，表示素数的个数。")
# ])
class Prime(BaseModel):
    prime: list[int] = Field(description="表示所有的素数")
    count: int = Field(description="素数的个数")


json_parser = JsonOutputParser(pydantic_object=Prime)
result = llm.invoke([
    ("system", json_parser.get_format_instructions()),
    ("user", "输出100之间所有素数")
])
print(result.content)
