from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

load_dotenv()

pdf_path= Path(__file__).parent/ "deeplearning.pdf"
data= PyPDFLoader(pdf_path)
docs= data.load()

splitter= RecursiveCharacterTextSplitter(
    chunk_size= 1000,
    chunk_overlap= 200
)

chunks= splitter.split_documents(docs)

template= ChatPromptTemplate.from_messages([
    ("system","You are a IA that summarizes the text"),
    ("human","{data}")
])

model= ChatMistralAI(model='mistral-large-latest')

prompt= template.format_messages(data= docs[0].page_content)

result= model.invoke(prompt)
print(result.content)
