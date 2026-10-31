"""
    测试：在Milvus数据库中创建集合
"""
from pymilvus import MilvusClient, DataType


# 获取连接Milvus的客户端对象
def get_milvus_client():
    return MilvusClient(url="http://localhost:19530")


# 获取Milvus中所有的集合
def get_milvus_collection(milvus_client: MilvusClient):
    result = milvus_client.list_collections()
    print(result)


# 创建集合
def create_collection(milvus_client: MilvusClient, collection_name: str):
    if not milvus_client.has_collection(collection_name):
        # 设置集合结构
        schema = milvus_client.create_schema(
            auto_id=True,
        )
        # 添加字段id
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        # 文本 text
        schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=2000)
        # 源数据 metadata
        schema.add_field(field_name="metadata", datatype=DataType.JSON)
        # 稠密向量 dense_vector
        schema.add_field(field_name="dense_vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
        # 稀疏向量 sparse_vector
        schema.add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)

        # 设置集合索引
        index_params = milvus_client.prepare_index_params()
        # 添加索引
        # 为稠密向量字段dense_vector添加索引
        index_params.add_index(
            field_name="dense_vector",  # 添加索引的字段名
            index_name="dense_index_index",  # 自定义索引名称
            index_type="HNSW",  # 设置索引的类型
            metric_type="L2"  # 设置计算相似度的方式(cosin,L2,IP)
        )
        # 为稀疏向量字段sparse_vector设置索引
        index_params.add_index(
            field_name="sparse_vector",  # 添加索引的字段名
            index_name="sparse_vector_index",  # 自定义索引名称
            index_type="SPARSE_INVERTED_INDEX",  # 设置索引的类型
            metric_type="IP"  # 设置计算相似度的方式(IP)
        )
        # 创建集合
        milvus_client.create_collection(
            collection_name=collection_name,
            schema=schema,
            index_params=index_params
        )


if __name__ == "__main__":
    milvus_client = get_milvus_client()
    create_collection(milvus_client, collection_name="collection_demo")
