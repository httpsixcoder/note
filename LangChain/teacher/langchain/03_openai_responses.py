import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASH_URL")
)
result = client.responses.create(
    model="qwen-flash",
    input=[
        {"role": "system", "content": "你是冷笑话高手"},
        {"role": "user", "content": "给我讲个笑话"}
    ]
)
print(result.output[0].content[0].text)
