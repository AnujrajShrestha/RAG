from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

pdf_path= Path(__file__).parent/ "GRU.pdf"

data= PyPDFLoader(pdf_path)
docs= data.load()

splitter= TokenTextSplitter(
    chunk_size=1000,
    chunk_overlap= 10
)

chunks= splitter.split_documents(docs)
print(chunks[0].page_content)