"""
    测试：使用HuggingFaceEmbeddings将文本转化为稠密向量
"""

# import torch
# print("GPU 是否可用:", torch.cuda.is_available())
# print("当前使用的设备:", torch.device("cuda" if torch.cuda.is_available() else "cpu"))
from langchain_huggingface import HuggingFaceEmbeddings

# 创建HuggingFaceEmbeddings对象
model=HuggingFaceEmbeddings(
    model_name='../../assets/models/bge-base-zh-v1.5',
)

# 使用本地嵌入模型将数据转换成稠密向量
result1=model.embed_query("你好，世界")
print(len(result1))
print(result1)
# 使用本地嵌入模型将数据转换成稠密向量
results2=model.embed_documents(["hello,LangChain","hello,LangGraph"])

print(len(results2))
print(len(results2[0]))
print(len(results2[1]))
for result in results2:
    print(len(result))
    print(result)
