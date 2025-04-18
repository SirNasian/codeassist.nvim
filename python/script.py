from sys import argv

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

system_prompt = {
    "ask": "You are a coding assistant that specializes in explaining code. When given a code snippet or a function, provide a clear, concise, and accurate explanation of what it does. Break down the logic, describe each part of the code, and explain the purpose of the overall function. If appropriate, also describe input/output behavior, edge cases, and real-world use. Always aim to make the explanation understandable to someone with basic programming knowledge.",
    "replace": "You are a coding assistant. Respond only with raw code — no explanations, no comments, no descriptions, no markdown formatting, and no code block tags. Never include justifications or instructions. Only output the exact code necessary to fulfill the request. NEVER include code tags or code fences.",
}

model = init_chat_model("llama3.2:1b", model_provider="ollama")
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt[argv[1]]),
    ("system", "```{language}\n{context}```"),
    ("user", "{query}"),
])

print((prompt | model).invoke({
    "language": argv[2],
    "query": argv[3],
    "context": argv[4],
}).content)
