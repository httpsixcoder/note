"""
    测试：加载word文档
"""
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

document = UnstructuredWordDocumentLoader(
    file_path="../../assets/sample.docx",
    mode="single"
).load()
print(type(document)) # <class 'list'>
print(document[0].metadata) # {'source': '../../assets/sample.docx'}
print(document[0])