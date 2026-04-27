"""
utils/llm.py
Returns a LangChain chat model pointed at 
  • Ollama local      (gemma4  model,             USE_OLLAMA=true)
"""
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


def get_llm():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = ChatOllama(
        model= "gemma4:e2b",
        base_url=base_url,
        temperature=0.2,
    )
    return model

model = get_llm()
print(model)