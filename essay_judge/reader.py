from langchain_community.document_loaders import TextLoader
import textract


def read_file(filepath: str) -> str:
    loader = textract.process(filepath)
    return loader.decode("utf-8")


# filepath = "../essays/The Importance of Sustainable Energy for a Resilient Future.docx"
# print(read_file(filepath))
