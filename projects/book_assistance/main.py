from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

embedding= MistralAIEmbeddings(model='mistral-embed')

vectorStore= Chroma(
    persist_directory='chroma-db',
    embedding_function=embedding
)

retriever= vectorStore.as_retriever(
    search_type='mmr',
    search_kwargs={
        "k":4,
        "fetch_k":10,
        "lambda_mult":0.5
    }
)

llm= ChatMistralAI(model="mistral-large-latest")

#prompt template
prompt= ChatPromptTemplate.from_messages([
    ('system',
     """You are a helpfull AI assistant.
     Use ONLY the provided context to answer the question.
     If the the answer is not present in the context,
     say: "I could not find the answer in the document."
     """
     ),('human',
        """Context:{context}
        Question: {question}""")
])

print("Rag system created")
print("Press 0 to exit")

while True:
    query= input("You: ")
    if query=="0":
        break
    docs= retriever.invoke(query)
    context= "\n\n".join([doc.page_content for doc in docs])
    
    final_prompt= prompt.invoke({
        'context': context,
        'question': query
    })
    
    response= llm.invoke(final_prompt)
    print(f"\n AI: {response.content}")
        