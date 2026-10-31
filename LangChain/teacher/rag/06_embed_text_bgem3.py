"""
    使用bgem3模型生成文本所对应的稠密向量和稀疏向量
"""
from FlagEmbedding import BGEM3FlagModel

# 获取模型对象
model = BGEM3FlagModel(
    model_name_or_path=r"../../bge-m3",
)
# 将文本转换成稠密向量和稀疏向量
result = model.encode(
    sentences=["我的天呀，啥时候可以回学校打排球呀呀呀"],  # 要转换为向量的文本
    return_dense=True,
    return_sparse=True,

)
# 获取稠密向量和稀疏向量
dense_vector=result["dense_vecs"][0]
sparse_vector=result["lexical_weights"][0]
#
# 打印稠密向量和稀疏向量
# print(dense_vector)
# print(sparse_vector)
# 将稀疏向量转换为token
# print(model.convert_id_to_token(sparse_vector))

print(result)
