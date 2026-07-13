from langchain_mistralai import MistralAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from pathlib import Path

load_dotenv()

pdf_path=Path(__file__).parent/ "deeplearning.pdf"
loader= PyPDFLoader(pdf_path)
docs= loader.load()

splitter= RecursiveCharacterTextSplitter(
    chunk_size= 2000,
    chunk_overlap= 200
)

chunks= splitter.split_documents(docs)

embeddings_model= MistralAIEmbeddings(model='mistral-embed')

vectorStore= Chroma.from_documents(
    documents= chunks,
    embedding= embeddings_model,
    persist_directory="summarizer_db"
)
