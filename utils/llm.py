"""Return the configured LangChain chat model."""
import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


def get_llm():
    model = ChatOllama(
        model= "llama3.1",
        temperature=0.2,
    )
    return model

model = get_llm()
