from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from rich import print
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

load_dotenv()

#1. Creatin tool

@tool
def get_text_length(text: str) -> int:
    """Return the number of character in a given text"""
    return len(text)

tools={
    'get_text_length': get_text_length
}

llm= ChatMistralAI(model='mistral-large-latest')

#tool binding
llm_with_tool= llm.bind_tools([get_text_length])

# result= llm_with_tool.invoke("Use the get_text_length tool to find the length of : hello how are you")

# if result.tool_calls:
#     tool_call= result.tool_calls[0]
#     tool_result= get_text_length.invoke(tool_call['args'])
    
# final_resopnse= llm.invoke(f"The length of the text is {tool_result}")

# print(final_resopnse.content)

message= []
query= HumanMessage("Return the number if characters in the given text: 'Hello how are you'")
message.append(query)

result= llm_with_tool.invoke(message)
print(result)

message.append(result)

if result.tool_calls:
    tool_name= result.tool_calls[0]['name']
    tool_message= tools[tool_name].invoke(result.tool_calls[0])
    message.append(tool_message)
    
result= llm_with_tool.invoke(message)

print(result.content)