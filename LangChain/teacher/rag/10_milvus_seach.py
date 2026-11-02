"""
    测试：混合检索
"""
import numpy as np
from FlagEmbedding import BGEM3FlagModel
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker


# 获取连接Milvus的客户端对象
def get_milvus_client():
    return MilvusClient(url="http://localhost:19530")


# client.query(...)：标量查询。用 id、文本、数字 去查，靠的是 CPU 扫描，不消耗显卡。
# client.search(...)：向量检索。用 向量 去查最相似的，靠的是索引（HNSW），这也是你下一步要写的核心代码！


# 检索数据
def embed_query(query: str):
    # 获取模型对象
    model = BGEM3FlagModel(
        model_name_or_path=r"../../bge-m3",
        devices="cuda:0"
    )

    # 将文本转换成稠密向量和稀疏向量
    result = model.encode(
        sentences=[query],  # 要转换为向量的文本
        return_dense=True,
        return_sparse=True,
    )

    dense_vec = np.array(result['dense_vecs'][0], dtype=np.float32).tolist()
    sparse_vec = {int(k): float(v) for k, v in result['lexical_weights'][0].items()}
    return dense_vec, sparse_vec


# 稠密向量检索
def milvus_search_by_dense(milvus: MilvusClient, collection_name: str, query: str):
    dense_vector, _ = embed_query(query)
    results = milvus_client.search(
        collection_name=collection_name,
        anns_field="dense_vector",  # 设置要检索的字段
        data=[dense_vector],  # 设置要检索的数据所对应的稠密向量
        search_params={"metric_type": "L2"},  # 设置计算相似度的方式
        output_fields=["id", "text", "metadata"],  # 设置输出字段
        limit=5  # 设置检索的数据条数
    )
    print(results)

    # # 💡 优化4：优雅地解析结果
    # for hits in results:
    #     for hit in hits:
    #         print(f"ID: {hit['id']} | 距离得分: {hit['distance']:.4f}")
    #         print(f"内容: {hit['entity']['text'][:50]}...\n")


# 稀疏向量检索
def milvus_search_by_sparse(milvus: MilvusClient, collection_name: str, query: str):
    _, sparse_vector = embed_query(query)
    results = milvus_client.search(
        collection_name=collection_name,
        anns_field="sparse_vector",  # 设置要检索的字段
        data=[sparse_vector],  # 设置要检索的数据所对应的稠密向量
        search_params={"metric_type": "IP"},  # 设置计算相似度的方式
        output_fields=["id", "text", "metadata"],  # 设置输出字段
        limit=5  # 设置检索的数据条数
    )
    print(results)
    # for hits in results:
    #     for hit in hits:
    #         print(f"ID: {hit['id']} | 内积得分: {hit['distance']:.4f}")
    #         print(f"内容: {hit['entity']['text'][:50]}...\n")


# 混合检索
def milvus_hybrid_search(milvus: MilvusClient, collection_name: str, query: str):
    # 将query转换成稠密向量和稀疏向量
    dense_vector, sparse_vector = embed_query(query)
    # 混合检索
    # 设置稠密向量检索的方式
    reqs_dens = AnnSearchRequest(
        data=[dense_vector],  # 设置要检索的数据所对应的稠密向量
        anns_field="dense_vector",  # 设置要检索的字段
        param={"metric_type": "L2"},  # 设置计算相似度的方式
        limit=5  # 设置检索的数据条数
    )
    # 设置稀疏向量检索的方式
    reqs_sparse = AnnSearchRequest(
        data=[sparse_vector],  # 设置要检索的数据所对应的稠密向量
        anns_field="sparse_vector",  # 设置要检索的字段
        param={"metric_type": "IP"},  # 设置计算相似度的方式
        limit=5  # 设置检索的数据条数
    )
    # 混合检索
    ressult = milvus_client.hybrid_search(
        collection_name=collection_name,
        reqs=[reqs_dens, reqs_sparse],
        ranker=RRFRanker(k=60),  # 设置重排序方式 【倒数】
        output_fields=["id", "text", "metadata"],
        limit=5,
    )
    print(ressult)


if __name__ == '__main__':
    milvus_client = get_milvus_client()
    # milvus_search_by_dense(milvus_client, collection_name="collection_demo", query="监护人需要旅行什么职责")
    # milvus_search_by_sparse(milvus_client, collection_name="collection_demo", query="监护人需要旅行什么职责")
    milvus_hybrid_search(milvus_client, collection_name="collection_demo", query="监护人需要旅行什么职责")
    """
    [   # 外层列表：代表第 1 个查询向量（因为你只查了一个 query，所以列表长度为 1）
        [   # 内层列表：代表命中的 Top-K 结果（按相似度排序，这里是前 2 个）
            {   # 第 1 条命中的结果（Milvus Hit 对象，长得像字典）
                "id": 470137222682620301, 
                "distance": 0.3456,        # 距离得分（L2 距离，越小越相似；IP/COSINE，越大越相似）
                "entity": {                # 你通过 output_fields 请求返回的字段
                    "text": "监护人应当履行抚养、教育和保护未成年人的职责...",
                    "metadata": {"source": "sample.docx", "start_index": 0}
                }
            },
            {   # 第 2 条命中的结果
                "id": 470137222682620302, 
                "distance": 0.5123,
                "entity": {
                    "text": "未成年人的父母是未成年人的监护人。如果父母已经死亡或者没有监护能力...",
                    "metadata": {"source": "sample.docx", "start_index": 120}
                }
            }
        ]
    ]
    """

    """
    更好的获取：假设 results 是你执行 search 得到的返回值 results = milvus.search(...)
    for hits in results:     # 第一层循环：遍历所有查询向量的结果（通常只有一个）
        for hit in hits:     # 第二层循环：遍历这个查询命中的 Top-K 结果
            # 1. 拿主键 ID
            doc_id = hit["id"]
            # 2. 拿得分
            score = hit["distance"]
            # 3. 拿具体字段（注意要先取 entity，再取里面的字段）
            text_content = hit["entity"]["text"]
            metadata = hit["entity"]["metadata"]
            print(f"得分: {score:.4f} | ID: {doc_id}")
            print(f"内容: {text_content[:30]}...")
            print("-" * 30)
    """
