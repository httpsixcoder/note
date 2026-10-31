"""

"""
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()

llm = init_chat_model("openai:qwen-flash")


class Prime(BaseModel):
    prime: list[int] = Field(description="表示所有的素数")
    count: int = Field(description="素数的个数")


llm = llm.with_structured_output(schema=Prime)
result = llm.invoke([
    ("user", "输出100以内的素数")
])
# print(type(result)) #Prime
print(result)
print(result.prime)
print(result.count)
