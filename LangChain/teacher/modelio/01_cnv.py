"""
    调用模型，需要两个数据 base_url 和 api_key
"""
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENAI_BASE_URL"))
