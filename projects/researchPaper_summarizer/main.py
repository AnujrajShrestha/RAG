from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm= ChatMistralAI(model="mistral-large-latest")
embedding_model= MistralAIEmbeddings(model='mistral-embed')

message=[]

prompt= ChatPromptTemplate.from_messages([
    ("system",
     """You are helpful AI assistant.
     Your task is to summarize large research by default
     and  Use ONLY the provided context to answer the question.
     If the answer is not present in the context,
     say: "I could not find the answer in the document." 
    """
     ),('human',
        """Context:{context}
        Question: {question}""")
])

prompt2= ChatPromptTemplate.from_messages([
    ("system",
     """You are helpful AI assistant.
     Your task is to summarize large research by default
    """
     ),('human',
        """Context:{context}
        Question: {question}""")
])

vectorStore= Chroma(
    persist_directory='summarizer_db',
    embedding_function= embedding_model
)

retriever= vectorStore.as_retriever(
    search_type='mmr',
    search_kwargs={
        "k":12,
        "fetch_k":20,
        "lambda_mult":0.5
    }
)

docs= retriever.invoke("Summarize the research paper in about 3 paragraphs")
context= "\n\n".join(doc.page_content for doc in docs)
summarizer= prompt2.invoke({
    'context': context,
    'question': "Summarize the research paper in about 3 paragraphs."
})
response= llm.invoke(summarizer)

print("----Summary of given research paper in 3 paragraphs----\n\n")
print(response.content)

print("\n----------How can I help you today ?-------------\n")
print("Type 0 to exit the application")

while True:
    query= input("You: ")
    if query=="0":
        break
    docs= retriever.invoke(query)
    context= "\n\n".join([doc.page_content for doc in docs])
    message.append({
        'role': 'user',
        'content': query
    })
    
    final_prompt= prompt.invoke({
        'context': context,
        'question': query
    })
    
    response= llm.invoke(final_prompt)
    message.append({
        'role': 'bot',
        'content': response.content
    })
    print(f"\n AI: {response.content}")