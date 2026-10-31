"""
    测试对文档切分
"""
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

documents = UnstructuredWordDocumentLoader(
    file_path="../../assets/sample.docx",
    mode="single"
).load()

#
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "!", "，", ""],
    chunk_size=400,  # 设置每一个切片的最大长度，默认4000
    chunk_overlap=20,  # 设置每一个切片的重叠长度，默认200
    length_function=len,  # 判断切片大小使用的函数，默认len
    add_start_index=True
    # 是否在切分之后的每个切片所对应的的Document对象中，
    # metadata属性是否存在start_index信息，表示每个切片对于整个文档的开始索引

)
chunk = splitter.split_documents(documents)
print(type(chunk))  # <class 'list'>
print(chunk)
print("============")
for doc in chunk:
    print(type(doc))  # <class 'langchain_core.documents.base.Document'>
    """
    返回的Document的结构
    # Document->metadata、page_content
        # metadata->source、start_index
            # source->../../assets/sample.docx
            # start_index->对应索引
        # page_content->切片内容
    """
    print(doc)
