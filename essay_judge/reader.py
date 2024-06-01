# from langchain_community.document_loaders import TextLoader
import textract
import os


def read_files(filepath: str) -> dict:
    collection = {}
    if not os.path.isdir(filepath):
        filename = os.path.basename(filepath)
        id = filename.split("_")[0]
        if filename.endswith(".docx"):
            essay = textract.process(filepath)
            collection[id] = essay.decode("utf-8")
            return collection
        
    for file in os.listdir(os.path.expanduser(filepath)):
        id = file.split("_")[0]
        if file.endswith(".docx"):
            essay = os.path.join(os.path.expanduser(filepath), file)
            essay = textract.process(essay)
            collection[id] = essay.decode("utf-8")

    return collection

"""
Collection = {
    "1": "Essay content 1",
    "2": "Essay content 2",
    ...
    "n": "Essay content n"
}
"""