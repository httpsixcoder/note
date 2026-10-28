"""
    示例：
    1.ChatCompletionsAPI
    2.ResponsesAPI
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client=OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASH_URL")
)
result=client.chat.completions.create(
    model="qwen-flash",
    messages=[
        { "role":"user","content":"给我讲个笑话"}
    ]
)
print(result.choices[0].message.content)
