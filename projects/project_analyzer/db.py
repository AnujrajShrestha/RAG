from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from pathlib import Path

load_dotenv()

model_embedding= MistralAIEmbeddings(model='mistral-embed')

directoryPath= str(Path(__file__).parent.parent/ "resume_info")

patterns = [
    "**/*.py", "**/*.js", "**/*.html", "**/*.css", 
    "**/*.md", "**/*.json", "**/*.txt", "**/*.php", 
    "**/*.jsx", "**/*.tsx", "**/*.c"
]

docs = []

for pattern in patterns:
    loader = DirectoryLoader(
        directoryPath,
        glob=pattern,
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        silent_errors=False,
    )
    docs.extend(loader.load())
    
splitter= RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap= 80
)

chunks= splitter.split_documents(docs)

vectorstore= Chroma.from_documents(
    documents= chunks,
    embedding=model_embedding,
    persist_directory="anaylzer_db"
)

print(len(docs))