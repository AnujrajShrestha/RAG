from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from rich import print

load_dotenv()

#1. Creatin tool

@tool
def get_text_length(text: str) -> int:
    """Return the number of character in a given text"""
    return len(text)

llm= ChatMistralAI(model='mistral-large-latest')

#tool binding
llm_with_tool= llm.bind_tools([get_text_length])

result= llm.invoke("hello")
print(result)

result2= llm_with_tool.invoke("Hello")
print(f"\n{result2}")