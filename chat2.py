import requests
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_groq import ChatGroq
import os
from langchain.agents import AgentExecutor, create_react_agent, load_tools

class WikipediaArticleExporter(BaseModel):
    article: str = Field(description="The canonical name of the Wikipedia article")

class GoogleMapsQuery(BaseModel):
    query: str = Field(description="Location or place to search for on Google Maps")

@tool("wikipedia_text_exporter", args_schema=WikipediaArticleExporter, return_direct=False)
def wikipedia_text_exporter(article: str) -> str:
    '''Fetches the most recent revision for a Wikipedia article in WikiText format.'''
    url = f"https://en.wikipedia.org/w/api.php?action=parse&page={article}&prop=wikitext&formatversion=2"

    result = requests.get(url).text
    start = result.find('"wikitext": "\{\{')
    end = result.find('\}</pre></div></div><!--esi')

    result = result[start+12:end-30]

    return ({"text": result})

@tool("google_maps_search", args_schema=GoogleMapsQuery)
def google_maps_search(query: str) -> str:
    """Search for a location or place on Google Maps and return its basic information."""
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    api_key = "AIzaSyC2Me226kdWfxFJHJbakNfKgtt5xN0QElY"  # Make sure to set this environment variable
    
    if not api_key:
        return "Error: Google Maps API key not found in environment variables"
    
    params = {
        "query": query,
        "key": api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        
        if data.get("results"):
            result = data["results"][0]
            return {
                "name": result.get("name", "N/A"),
                "address": result.get("formatted_address", "N/A"),
                "rating": result.get("rating", "N/A"),
                "location": result.get("geometry", {}).get("location", {})
            }
        return "No results found"
    except Exception as e:
        return f"Error searching Google Maps: {str(e)}"

def append_chat_history(input, response):
    chat_history.save_context({"input": input}, {"output": response})

def invoke(input):
    msg = {
        "input": input,
        "chat_history": chat_history.load_memory_variables({}),
    }
    print(f"Input: {msg}")

    response = agent_executor.invoke(msg)
    print(f"Response: {response}")

    append_chat_history(response["input"], response["output"])
    print(f"History: {chat_history.load_memory_variables({})}")

# tools = [google_maps_search]
prompt = hub.pull("hwchase17/react-chat")
print(prompt)

os.environ["GROQ_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "91945fee4ad7927dca0e9e523a9f3be1b7263ec591be20d7135ceff75feb0d4a"

llm = ChatGroq(model="llama3-8b-8192")

tools = load_tools(
    ["serpapi"],
)
chat_history = ConversationBufferWindowMemory(k=10)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

user_input = input("Input")
invoke(user_input)