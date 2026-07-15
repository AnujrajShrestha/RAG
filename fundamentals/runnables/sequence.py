from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableLambda

load_dotenv()

prompt= ChatPromptTemplate.from_template(
    'Explain {topic} in simple words'
)

short_prompt= ChatPromptTemplate.from_template(
    'Give short defination of {topic}'
)

model= ChatMistralAI(model='mistral-large-latest')

parser= StrOutputParser()

fromatted_prompt= prompt.format_messages(topic='Machine Learning')


#sequential runnable
chain= prompt | model | parser

result= chain.invoke("Machine Learning")
print(result)

#paralle runnable
chain_dict=RunnableParallel({
    "short": short_prompt | model | parser,
    'detailed': prompt | model | parser
})

chain_dict.invoke({'topic': 'Machine Learning'})

#runnable Lambda
chain= RunnableParallel({
    'short': RunnableLambda(lambda x: x['short']) | short_prompt | model | parser,
    'detailed': RunnableLambda(lambda x: x['detailed']) | prompt | model | parser
})

chain.invoke({
    'short': {'topic': 'Machine Learning'},
    'detailed': {'topic': 'Deep Learning'}
}) 

#runnable passthrough
