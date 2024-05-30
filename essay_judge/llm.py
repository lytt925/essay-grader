from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

chatModel = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)


prompt = ChatPromptTemplate.from_messages([
    ("system", "請就這篇文章的文章內容、文章結構和英文文法，給一個60-100字的台灣繁體中文評語，並給出分數。"),
    ("user", "「{input}」")
])

chain = prompt | chatModel