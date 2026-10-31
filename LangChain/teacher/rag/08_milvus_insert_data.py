"""
    测试：在Milvus数据库中创建集合
"""
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel
import numpy as np # 确保导入 numpy


# 获取连接Milvus的客户端对象
def get_milvus_client():
    return MilvusClient(url="http://localhost:19530")


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
            # 强制转换为 float32 的 numpy 数组
            # "dense_vector": dense_vector,
            "dense_vector": np.array(dense_vector, dtype=np.float32),
            "sparse_vector": sparse_vector,
        })
    # 存储数据
    milvus_client.insert(
        collection_name=collection_name,
        data=data
    )


if __name__ == "__main__":
    milvus_client = get_milvus_client()
    insert_data(milvus_client, "collection_demo")
