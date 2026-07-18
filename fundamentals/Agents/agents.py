from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import AIMessage,HumanMessage,ToolMessage
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
import os
import requests
from rich import print

load_dotenv()


# Weather tool
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    api_key= os.getenv("OPENWEATHER_API_KEY")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},NP&appid={api_key}&units=metric"
    
    response= requests.get(url)
    data= response.json()
    
    # print("DEBUG: ",data)
    
    if str(data.get("cod")) !="200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"
    
    temp= data["main"]["temp"]
    desc= data["weather"][0]["description"]
    
    return f"Weather on {city}: {desc}, {temp}°C"

# print(get_weather.invoke("Butwal"))

tavily_client= TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#News tool
@tool
def get_news(city: str) -> str:
    """Get lastest news about the city"""
    
    response= tavily_client.search(
        query=f"latest news in {city}",
        search_depth='basic',
        max_results=3
    )
    
    results= response.get("result",[])
    
    if not results:
        return f"No news found for {city}"
    
    news_list= []
    
    for r in results:
        title= r.get("title","No title")
        url= r.get("url", "")
        snippet= r.get("content", "")
        
        news_list.append(f"- {title}\n {url}\n {snippet[:100]}...")
        
    return f"Latest news in {city}:\n\n"+ "\n\n".join(news_list)

# print(get_news.invoke("Kathmandu"))

llm= ChatMistralAI(model="mistral-large-latest")

# tools={
#     "get_weather": get_weather,
#     "get_news": get_news
# }

# llm_with_tool= llm.bind_tools([get_weather,get_news])

# #Agent loop
# messages= []
# print("City intelligence system")
# print("type Exit to quit")

# while True:
#     user_input= input("You: ")
#     if user_input.lower() == "exit":
#         break
#     messages.append(HumanMessage(content= user_input))
    
#     while True:
#         result= llm_with_tool.invoke(messages)
        
#         messages.append(result)
        
#         #if tool is required
#         if result.tool_calls:
#             for tool_call in result.tool_calls:
#                 tool_name= tool_call['name']
#                 #human in the loop
#                 confirm= input(f"Agent wants to call {tool_name} Approve (yes/no): ")
                
#                 if confirm.lower() == "no":
#                     print("Tool call deniend and I cannot get the latest information")
                
#                 #execute tool
#                 tool_result= tools[tool_name].invoke(tool_call)
                
#                 messages.append(ToolMessage(
#                     content=tool_result,
#                     tool_call_id= tool_call['id']
#                 ))
#             continue
        
#         else:
#             print("\n Final answer: \n")
#             print(result.content)
#             print("\n"+ "="*50+ "\n")
#             break

#hitory message
store= []

def store_messages(role,inp):
    if role.lower()== 'user':
        store.append({
            'role':role,
            'content': inp
        })
    elif role.lower()== 'assistant':
        store.append({
            'role': role,
            'content': inp
        })

@wrap_tool_call
def human_approval(request,handler):
    """Ask for human approval before every tool call."""
    tool_name= request.tool_call['name']
    confirm= input(f"Agent want to call '{tool_name}.' Approve? (yes/no): ")
    
    if confirm.lower() == "no":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id= request.tool_call['id']
        )
    return handler(request)

agent= create_agent(
    llm,
    tools= [get_weather,get_news],
    system_prompt="You are a helpful city assistant.",
    middleware= [human_approval],
)

print("City Agent | Type exit to quit") 

while True:       
    user_input= input("You: ")
    store_messages('user',user_input)
    if user_input.lower() =="exit":
        break
    result= agent.invoke({
        "messages":store
    })
    
    store_messages('assistant',result['messages'][-1].content)
    print(f"Bot: {result['messages'][-1].content}")