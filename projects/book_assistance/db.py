#load pdf
#split into chunks
#create the embeddings
#store into chroma

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

pdf_path= Path(__file__).parent/ "deeplearning.pdf"
loader= PyMuPDFLoader(pdf_path)
docs= loader.load()

splitter= RecursiveCharacterTextSplitter(
    chunk_size= 1000,
    chunk_overlap= 200
)

chunks= splitter.split_documents(docs)

embedding_model= MistralAIEmbeddings(model='mistral-embed')

vectorStore= Chroma.from_documents(
    documents= chunks,
    embedding= embedding_model,
    persist_directory="chroma-db"
)