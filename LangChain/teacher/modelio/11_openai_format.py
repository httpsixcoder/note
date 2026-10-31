"""
    测试：使用OpenAI原生API实现输出格式化
"""
import os

from dotenv import load_dotenv
from openai import OpenAI
# from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)


class Prime(BaseModel):
    prime: list[int] = Field(description="表示所有的素数")
    count: int = Field(description="素数的个数")


result = client.chat.completions.parse(
    model="qwen-flash",
    messages=[
        {
            "role": "user",
            "content": "获得1-100之间的素数"
        }
    ],
    # 设置输出格式化，
    response_format=Prime,
)
print(result.choices[0].message.content)
