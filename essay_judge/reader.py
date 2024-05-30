from langchain_community.document_loaders import TextLoader

def read_file(filepath: str) -> str:
    loader = TextLoader("./essay.md")
    return loader.load()[0].page_content

