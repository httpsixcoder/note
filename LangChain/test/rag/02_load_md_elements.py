from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader=UnstructuredMarkdownLoader(
    file_path="../../assets/sample.md",
    mode="elements"
)
elements = loader.load()
# print(type(elements)) #<class 'list'>
for element in elements:
    print(element)