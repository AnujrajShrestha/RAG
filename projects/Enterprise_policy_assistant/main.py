from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma

load_dotenv()

embedding= MistralAIEmbeddings(model='mistral-embed')

vectorStore= Chroma(
    persist_directory='Entreprise_db',
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

message=[
    SystemMessage(content=f"You are a helpfull AI assistant you have give answers to our company empolyees politely")
]

prompt= ChatPromptTemplate.from_messages([
    ('system',
     """You are a helpfull AI assistant.
     Use ONLY the provided context to answer the question.
     If the the answer is not present in the context,
     say: "I could not find the answer in the document." (Your response should be mainly focus on company related)
     """
     ),('human',
        """Context:{context}
        Question: {question}""")
])

print("\n----------How can I help you today ?-------------\n")
print("Type 0 to exit the application")

while True:
    query= input("You: ")
    if query=="0":
        break
    docs= retriever.invoke(query)
    context= "\n\n".join([doc.page_content for doc in docs])
    message.append(HumanMessage(content=query))
    
    final_prompt= prompt.invoke({
        'context': context,
        'question': query
    })
    
    response= llm.invoke(final_prompt)
    message.append(AIMessage(content=response.content))
    print(f"\n AI: {response.content}")