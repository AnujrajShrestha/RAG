from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from pydantic import BaseModel,Field
from typing import List,Optional
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

llm= ChatMistralAI(model='mistral-large-latest',temperature=0.0)
embedding_model= MistralAIEmbeddings(model='mistral-embed')

message=[
    SystemMessage(content="You are a helpful AI assistant, your task is to analyis the files")
]

class FolderAnalysis(BaseModel):
    project_name: str = Field(description="The name of the software project or repository.")
    files: List[str] = Field(description="An explicit list of all file names found in the context.")
    path: Optional[str] = Field(description="The absolute or relative directory path of the folder analyzed.")
    summary: str = Field(description="A thorough, cohesive technical overview of what these files collectively do.")
    suggestions: str = Field(description="Constructive architectural or code-quality improvement recommendations.")
    
parser = PydanticOutputParser(pydantic_object=FolderAnalysis)

prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        """You are an expert Principal Software Engineer and static code analyst.
Your task is to analyze a collection of project files provided in the context and extract structural information, a comprehensive summary, and targeted development suggestions.

CRITICAL INSTRUCTIONS:
1. Base your summary and suggestions *only* on the provided file contents. Do not assume dependencies or architecture not visible in the text.
2. The 'suggestions' field should contain actionable engineering feedback (e.g., performance fixes, security issues, formatting issues, or structural patterns).
3. You must format your output exactly according to the pdf format

{format_instructions}"""
    ),
    (
        "human",
        """Review the codebase snapshot provided below and complete the structured analysis.

[START CODEBASE CONTEXT]
{context}
[END CODEBASE CONTEXT]

User Objective/Question:
{question}
"""
    )
])

chat_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a senior technical advisor and project co-pilot. 
Your goal is to answer the user's questions about their codebase while proactively providing actionable engineering suggestions.

OPERATIONAL GUIDELINES:
1. **Analyze with Context:** Use the provided codebase context to answer the user's technical questions accurately.
2. **Proactive Suggestions:** In every response, look for opportunities to offer relevant code-quality, architectural, or optimization suggestions related to their query.
3. **Be Specific:** Reference actual file names, functions, or patterns found in the context when making suggestions. Avoid generic advice like "write clean code."
4. **Honesty:** If the user asks about a part of the project not present in the provided context, state that you don't have visibility into that file or module.

[START CODEBASE CONTEXT]
{context}
[END CODEBASE CONTEXT]"""
    ),MessagesPlaceholder(variable_name="chat_history"),
    (
        "human",
        "{question}"
    )
])

vectorStore= Chroma(
    persist_directory='anaylzer_db',
    embedding_function= embedding_model
)

retriever= vectorStore.as_retriever(
    search_type='mmr',
    search_kwargs={
        "k":8,
        "fetch_k":12,
        "lambda_mult":0.5
    }
)

docs= retriever.invoke("provide the information,summary and suggestion of this project.")
context= "\n\n".join(doc.page_content for doc in docs)
summarizer= prompt.invoke({
    'context': context,
    'question': "provide the information,summary and suggestion of this project.",
    "format_instructions": parser.get_format_instructions()
})
message.append(HumanMessage(content="provide the information,summary and suggestion of this project."))
response= llm.invoke(summarizer)
final_res= parser.parse(response.content)
message.append(AIMessage(content=response.content))

print("\n========== Project Information ==========\n")

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
        'question': query,
        'chat_history': message
    })
    
    response= llm.invoke(final_prompt)
    message.append(AIMessage(content=response.content))
    print(f"\n AI: {response.content}")