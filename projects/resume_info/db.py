from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from pathlib import Path

load_dotenv()

embedding_model= MistralAIEmbeddings(model='mistral-embed')
txt_path= Path(__file__).parent/  "resume.txt"
loader= TextLoader(txt_path,encoding='utf-8')
docs= loader.load()

splitter= RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)

chunks= splitter.split_documents(docs)

vectorStore= Chroma.from_documents(
    documents= chunks,
    embedding= embedding_model,
    persist_directory='resume_db'
)

