"""
    使用HuggingFaceEmbeddings对文本进行（稠密）向量的转换
"""
from langchain_huggingface import HuggingFaceEmbeddings

model = HuggingFaceEmbeddings(
    model_name=r"../../assets/models/bge-base-zh-v1.5",
    # model_kwargs={'device': device_type},
    # model_kwargs={'device': 'cuda'},  # 👈 强行召唤显卡
    # encode_kwargs={'normalize_embeddings': True}  # 👈 BGE 模型标配：向量归一化，算相似度更准
)

result1 = model.embed_query("你好，美食")
result2 = model.embed_documents(["1","2","3"])
print(len(result1))
print(result1)
print(len(result2))
print(len(result2[0]))
print(result2)
