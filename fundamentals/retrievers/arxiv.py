from dotenv import load_dotenv
from langchain_community.retrievers import ArxivRetriever

load_dotenv()

# Initialize the correct ArxivRetriever
retriever = ArxivRetriever(
    load_max_docs=2,
    load_all_available_meta=True
)

docs = retriever.invoke("large language models")

for i, doc in enumerate(docs):
    print(f"\nResult: {i+1}")
    print("Title:", doc.metadata.get("Title"))
    print("Authors:", doc.metadata.get("Authors"))
    # ArxivRetriever puts the summary/abstract directly into page_content
    print("Summary:", doc.page_content[:500])