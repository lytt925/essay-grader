from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

chatModel = ChatOpenAI(model="gpt-4o", temperature=0.01)


# Build templates
system_template = """
請根據以下指令批改文章：
「{instruction}」
"""

human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template),
])

prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "「{input}」")
])

chain = prompt | chatModel
