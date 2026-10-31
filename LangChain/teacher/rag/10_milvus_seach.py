"""
    测试：混合检索
"""
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel
from sympy.series import limits


# 获取连接Milvus的客户端对象
def get_milvus_client():
    return MilvusClient(url="http://localhost:19530")


# 检索数据
def embed_query(query: str):
    # 获取模型对象
    model = BGEM3FlagModel(
        model_name_or_path=r"../../bge-m3",
    )

    # 将文本转换成稠密向量和稀疏向量
    result = model.encode(
        sentences=[query],  # 要转换为向量的文本
        return_dense=True,
        return_sparse=True,
    )
    return result['dense_vecs'][0], result['lexical_weights'][0]

# 稠密向量检索
def milvus_search_by_dense(milvus: MilvusClient, collection_name: str, query: str):
    dense_vector, _ = embed_query(query)
    results = milvus_client.search(
        collection_name=collection_name,
        anns_field="dense_vector",  # 设置要检索的字段
        data=[dense_vector],  # 设置要检索的数据所对应的稠密向量
        search_params={"metric_type": "L2"},  # 设置计算相似度的方式
        output_fields=["id", "text", "metadata"],  # 设置输出字段
        limits=5  # 设置检索的数据条数
    )
    print(results)

# 稀疏向量检索
def milvus_search_by_sparse(milvus: MilvusClient, collection_name: str, query: str):
    _, sparse_vector = embed_query(query)
    results = milvus_client.search(
        collection_name=collection_name,
        anns_field="sparse_vector",  # 设置要检索的字段
        data=[sparse_vector],  # 设置要检索的数据所对应的稠密向量
        search_params={"metric_type": "IP"},  # 设置计算相似度的方式
        output_fields=["id", "text", "metadata"],  # 设置输出字段
        limits=5  # 设置检索的数据条数
    )
    print(results)


if __name__ == '__main__':
    milvus_client = get_milvus_client()
    milvus_search_by_dense(milvus_client, collection_name="collection_demo", query="监护人需要旅行什么职责")
    """
    [
        [
        {id:xxx,}
        {id:xxx,}
        ]
    ]
    """
    milvus_search_by_sparse(milvus_client, collection_name="collection_demo", query="监护人需要旅行什么职责")
