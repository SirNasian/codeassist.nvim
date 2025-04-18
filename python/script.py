from sys import argv

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

model = init_chat_model("llama3.2:1b", model_provider="ollama")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your purpose is to assist the user with any {language} code queries they may have."),
    ("system", "Keep your answers short and cocise, mainly focusing on providing code snippets."),
    ("system", "Use the following context to help the user with their query: {context}"),
    ("user", "query: {query}"),
])

print((prompt | model).invoke({
    "language": argv[1] if len(argv) > 1 else "",
    "query": argv[2] if len(argv) > 2 else "",
    "context": argv[3] if len(argv) > 3 else "",
}).content)
