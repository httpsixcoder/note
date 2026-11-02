"""
    测试：RAG最终步骤，将检索的最终片段和用户的问题一起发送到大模型，由大模型总结输出
"""
import numpy as np
from FlagEmbedding import BGEM3FlagModel
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker

load_dotenv()
# 获取模型对象
print("正在加载 BGE-M3 模型...")
model = BGEM3FlagModel(
    model_name_or_path=r"../../bge-m3",
    devices="cuda:0",
    use_fp16=True
)


# 获取连接Milvus的客户端对象
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")


# 检索数据
def embed_query(query: str):
    # 将文本转换成稠密向量和稀疏向量
    result = model.encode(
        sentences=[query],  # 要转换为向量的文本
        return_dense=True,
        return_sparse=True,
    )

    dense_vec = np.array(result['dense_vecs'][0], dtype=np.float32).tolist()
    sparse_vec = {int(k): float(v) for k, v in result['lexical_weights'][0].items()}
    return dense_vec, sparse_vec


# 混合检索
def milvus_hybrid_search(milvus_client: MilvusClient, collection_name: str, query: str):
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
        ranker=RRFRanker(k=60),  # 设置重排序方式 【倒数排名融合】
        output_fields=["id", "text", "metadata"],
        limit=5,
    )
    # print(ressult)
    return ressult


# 获取最重大模型总结的结果

def llm_final_answer():
    milvus_client = get_milvus_client()
    collection_name = "collection_demo"
    query = "监护人需要旅行什么职责"

    # 获取混合检索的结果
    results = milvus_hybrid_search(milvus_client, collection_name=collection_name, query=query)
    # 获取检索中切片的文本
    texts = [chunk["entity"]["text"] for chunk in results[0]]
    # 拼接切片中的文本作为上下文
    context = "\n".join(texts)
    # 设置提示词
    message_list = [
        {"role": "system",
         "content": "你是一个专业的法律问答机器人，请根据上下文回答问题，当上下文无法回答问题时，请回答“根据上下文无法回答该问题”"},
        {"role": "user", "content": f"根据以下上下文回答问题：{context}\n问题：{query}"}
    ]

    # llm
    llm = init_chat_model("openai:qwen-flash")
    final_answer = llm.invoke(message_list)

    # print(final_answer)
    print("\n========== 🤖 大模型最终回答 ==========")
    print(final_answer.content)  # 💡 只打印纯文本内容
    print("======================================\n")


if __name__ == '__main__':
    llm_final_answer()
