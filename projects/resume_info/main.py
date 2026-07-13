from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel
from typing import List,Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

llm= ChatMistralAI(model='mistral-large-latest')
embedding_model= MistralAIEmbeddings(model='mistral-embed')

message=[
    SystemMessage(content="You are a helpful AI assistant your task is to analyse resumes")
]

class answer(BaseModel):
    name: str
    address: str
    email: Optional[str]= None
    number: Optional[str]= None
    Education: str
    GitHub: Optional[str]= None
    LinkedIn: Optional[str]= None
    Portfolio: Optional[str]= None
    skills: List[str]
    projects: Optional[List[str]]= None
    certificates: Optional[List[str]]= None
    achievements: Optional[List[str]]= None
    soft_skills: List[str]
    language: List[str]
    Summary: str
    suggestion: str
    questions: List[str]
    
parser= PydanticOutputParser(pydantic_object=answer)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful AI assistant.

Your task is to analyze the given resume.

Extract all available information.


Also:
- Summarize the resume.
- Suggest improvements.
- Ask 5 interview questions.

{format_instructions}
"""
    ),
    (
        "human",
        """
Context:
{context}

Question:
{question}
"""
    )
])

chat_prompt= ChatPromptTemplate.from_messages([
    ('system',
     """You are a helpful AI assistant.
     your task is to analyse the given resume
       and  Use ONLY the provided context to answer the question.
     If the answer is not present in the context,
     say: "I could not find the answer in the document." 
     """
     ),('human',
        """Context:{context}
        Question: {question}""")
])

vectorStore= Chroma(
    persist_directory='resume_db',
    embedding_function= embedding_model
)

retriever= vectorStore.as_retriever(
    search_type='mmr',
    search_kwargs={
        "k":4,
        "fetch_k":10,
        "lambda_mult":0.5
    }
)

docs= retriever.invoke("provide the information of this resume.")
context= "\n\n".join(doc.page_content for doc in docs)
summarizer= prompt.invoke({
    'context': context,
    'question': "provide the information of this resume.",
    "format_instructions": parser.get_format_instructions()
})
message.append(HumanMessage(content="provide the information of this resume."))
response= llm.invoke(summarizer)
final_res= parser.parse(response.content)
message.append(AIMessage(content=response.content))

print("\n========== Resume Information ==========\n")

for key, value in final_res.model_dump().items():
    print(f"{key}:")
    print(value)
    print("-" * 50)

print("\n----------How can I help you today ?-------------\n")
print("Type 0 to exit the application")

while True:
    query= input("You: ")
    if query=="0":
        break
    docs= retriever.invoke(query)
    context= "\n\n".join([doc.page_content for doc in docs])
    message.append(HumanMessage(content=query))
    
    final_prompt= chat_prompt.invoke({
        'context': context,
        'question': query
    })
    
    response= llm.invoke(final_prompt)
    message.append(AIMessage(content=response.content))
    print(f"\n AI: {response.content}")