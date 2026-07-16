from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

search_tool= TavilySearchResults(max_result=5)

llm= ChatMistralAI(model= 'mistral-large-latest')

prompt= ChatPromptTemplate.from_template(
    """You are a hrlpful assistant
    
    summarizer the following news into clear bullet
    points
    {news}"""
)

chain= prompt | llm | StrOutputParser()

newsResult= search_tool.run("Latest AI news of 2026")

result= chain.invoke({'news': newsResult})

print(result)