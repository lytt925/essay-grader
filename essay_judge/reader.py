# from langchain_community.document_loaders import TextLoader
import textract
import os


def read_file(filepath: str) -> dict:
    collection = {}
    for file in os.listdir(filepath):
        id = file.split("_")[0]

        if file.endswith(".docx"):
            essay = os.path.join(filepath, file)
            essay = textract.process(essay)
            collection[id] = essay.decode("utf-8")

    return collection


# filepath = "../essays/"
# print(read_file(filepath))
