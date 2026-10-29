from langchain_community.document_loaders import UnstructuredWordDocumentLoader

loader = UnstructuredWordDocumentLoader(
    file_path="../../assets/sample.docx",
)

documents = loader.load()
print(documents[0])
