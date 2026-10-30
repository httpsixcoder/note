"""
    测试：使用RecursiveCharacterTextSplitter进行文档切分
"""
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 读取文档
documents = UnstructuredWordDocumentLoader(
    file_path="../../assets/sample.docx",
    mode="single"
).load()

# 创建递归切分对象
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "，"],  # 分隔符
    chunk_size=400,  # 每个切片大小
    chunk_overlap=50,  # 设置重复的字符数
    length_function=len,  # 计算切片大小所用的函数
    add_start_index=True  # 是否为每个切片添加start_index属性，记录当前切片在整个文档中的起始索引
)
# 切分文档

chunk = splitter.split_documents(documents)

for doc in chunk:
    print(doc)
