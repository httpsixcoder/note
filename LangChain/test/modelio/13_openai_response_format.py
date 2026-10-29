import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
# 创建模型对象
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


# 创建模型类
class JieRi(BaseModel):
    jieri: list[str]
    descriptions: list[str]


# 调用模型
resp = client.chat.completions.parse(
    model="qwen-flash",
    messages=[
        {"role": "user", "content": "查询一年中的重要节日，以及节日描述"}
    ],
    response_format=JieRi
)

print(resp.choices[0].message.parsed)
