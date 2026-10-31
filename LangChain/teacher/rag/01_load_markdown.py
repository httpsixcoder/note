"""
    测试：加载MarkDown文档
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# # 加载一个md文档为一个Document对象
# document = UnstructuredMarkdownLoader(
#     file_path="../../assets/sample.md",
#     mode="single"
# ).load()
# 加载一个md文档为多个Document对象
documents = UnstructuredMarkdownLoader(
    file_path="../../assets/sample.md",
    mode="elements"
).load()

for document in documents:
    print(document)
