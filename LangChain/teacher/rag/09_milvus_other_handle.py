"""
    测试：Milvus中的其他操作
"""
from pymilvus import MilvusClient


# 获取连接Milvus的客户端对象
def get_milvus_client():
    return MilvusClient(url="http://localhost:19530")


# 删除数据
def delete_data(milvus_client: MilvusClient, collection_name: str):
    milvus_client.delete(
        collection_name=collection_name,
        # filter="id ==  470137222682620301"
        filter="id in  [470137222682620302,470137222682620303]"
    )


# 检索数据
def query_data(milvus_client: MilvusClient, collection_name: str):
    res = milvus_client.query(
        collection_name=collection_name,
        # filter="id ==  470137222682620304",
        filter="text like '%监护人%' ",
        output_fields=["id", "text"]
    )
    print(res)


if __name__ == '__main__':
    milvus_client = get_milvus_client()
    # delete_data(milvus_client, collection_name="collection_demo")
    query_data(milvus_client, collection_name="collection_demo")
