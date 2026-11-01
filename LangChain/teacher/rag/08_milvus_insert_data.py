"""
    测试：在Milvus数据库中创建集合
"""
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel
import numpy as np  # 确保导入 numpy


# 获取连接Milvus的客户端对象
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")


# 向Milvus中添加数据
def insert_data(milvus_client: MilvusClient, collection_name: str):
    # 加载文档
    documents = UnstructuredWordDocumentLoader(
        file_path="../../assets/sample.docx"
    ).load()

    # 切分文档
    chunks = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "，", ""],
        chunk_size=400,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    ).split_documents(documents)
    # 将每个切片的文本存储到一个列表中
    chunks = chunks[:30]
    sentences = [chunk.page_content for chunk in chunks]
    # 获取模型对象
    model = BGEM3FlagModel(
        model_name_or_path=r"../../bge-m3",
        # 文本语义检索推荐use_fp16，16位，科学计算火箭什么的需要高精度的
        # 开启半精度，省显存且提速
        # use_fp16=True,
        # cuda 代表显卡，:0 代表第 0 号显卡
        devices="cuda:0"
    )
    # 生成向量
    embed_result = model.encode(
        sentences=sentences,
        return_dense=True,
        return_sparse=True,
    )
    # 分别获取所有切片的稠密向量和稀疏向量
    dense_vector_list = embed_result["dense_vecs"]
    sparse_vector_list = embed_result["lexical_weights"]
    # 创建存储最终数据的列表
    data = []
    # 循环chunks，dense_vector_list，sparse_vector_list组装要添加到milvus中数据【拉链式打包】
    for chunk, dense_vector, sparse_vector in zip(chunks, dense_vector_list, sparse_vector_list):
        data.append({
            "text": chunk.page_content,
            "metadata": chunk.metadata,
            # 保证兼容性.tolist()
            "dense_vector": np.array(dense_vector, dtype=np.float32).tolist(),
            "sparse_vector": {int(k): float(v) for k, v in sparse_vector.items()},
        })

        """
        # "dense_vector": dense_vector,
            BGE-M3 底层吐出来的是 np.ndarray（numpy 数组），而且如果你开了 fp16，里面装的是 float16。
            Milvus 底层的 C++ 引擎（特别是 HNSW 索引）对数据类型极其死板,只认识 float32 的数组
            也不一定能完美兼容所有版本的 numpy 对象，直接塞必报错。把 16 位的精度强行转换成 32 位格式（补零）
        # "sparse_vector": sparse_vector,
            Sparse：BGE-M3 吐出来的是 defaultdict(<class 'int'>, {'6688': 0.45})。
            注意：这里的键（Key）是字符串 "6688"！ 
            但 Milvus 的稀疏向量索引（倒排索引）要求 Key 必须是纯整数（int），否则底层的哈希表没法建。
        """
    # 存储数据
    res = milvus_client.insert(
        collection_name=collection_name,
        data=data
    )
    print(f"✅ 数据插入成功！共插入 {res['insert_count']} 条。")


if __name__ == "__main__":
    milvus_client = get_milvus_client()
    insert_data(milvus_client, "collection_demo")
