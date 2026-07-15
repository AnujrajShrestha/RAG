from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()

llm= ChatMistralAI(model='mistral-large-latest')
parser= StrOutputParser()

code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code generator"),
    ("human", "{topic}")
])

explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who explains code in simple terms"),
    ("human", "Explain the following code in simple words:\n{code}")
])

seq= code_prompt | llm | parser | explain_prompt | llm | parser

seq2= code_prompt | llm | parser

seq3= RunnableParallel({
    "code": RunnablePassthrough(),
    "expanation": explain_prompt | llm | parser 
})

chain= seq2 | seq3
result= chain.invoke({'topic': "write a palindrome code ein python"})

print(result['code'])
print(result['expanation'])