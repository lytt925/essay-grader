from langchain_community.document_loaders import TextLoader

def read_file(filepath: str) -> str:
    loader = TextLoader(filepath)
    return loader.load()[0].page_content

