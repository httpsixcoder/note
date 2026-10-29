"""
    1.由于API_KEY和BASH_URL属于敏感信息，不建议直接硬编码到代码中
    建议将这些敏感信息储存到.env文件中，其中以key=value的格式保存数据
    2.读取.env文件中的内容，使用os.getenv(key)读取环境变量
        1).os.getenv(key)默认读取系统的环境变量
        2).若需要读取.env中的环境变量，则需要load_dotenv()加载
        3).若系统环境变量中和.env环境变量中同时存在相同的键值对，则默认获取系统中环境变量key所对应的value
        4).若系统环境变量中和.env环境变量中同时存在相同的键值对，需要优先获取.env文件中的内容
        可以在load_dotenv()中太牛加参数override=True，表示将.env文件中的key和value覆盖系统环境变量中的key和value
"""
import os

from dotenv import load_dotenv

# 加载.env文件中的内容到环境变量
load_dotenv(
    override=True,  # 将.env文件中的key和value覆盖系统环境变量中的key和value
)


api_key = os.getenv("OPENAI_API_KEY")
print(api_key)
bash_url = os.getenv("OPENAI_BASH_URL")
print(bash_url)
