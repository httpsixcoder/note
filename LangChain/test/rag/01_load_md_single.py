from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader(
    file_path="../../assets/sample.md",
    mode="single"
)

elements = loader.load()
# print(type(elements)) #<class 'list'>
print(elements[0].page_content)
