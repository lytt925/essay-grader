from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

chatModel = ChatOpenAI(model="gpt-4o", temperature=0.01)

# Build templates
system_template = """
請根據以下指令批改文章,
首先先給一個總分數(滿分20分)，接著給出評語，先提優點再提缺點，並根據問題給出建議或修正，最後再給適當鼓勵
「{instruction}」

請將你的所有回應以html格式寫出。
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "「{input}」")
])

chain = prompt | chatModel
