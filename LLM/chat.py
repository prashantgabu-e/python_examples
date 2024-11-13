import requests

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_groq import ChatGroq
import os
class WikipediaArticleExporter(BaseModel):
    article: str = Field(description="The canonical name of the Wikipedia article")

@tool("wikipedia_text_exporter", args_schema=WikipediaArticleExporter, return_direct=False)
def wikipedia_text_exporter(article: str) -> str:
  '''Fetches the most recent revision for a Wikipedia article in WikiText format.'''
  url = f"https://en.wikipedia.org/w/api.php?action=parse&page={article}&prop=wikitext&formatversion=2"

  result = requests.get(url).text
  start = result.find('"wikitext": "\{\{')
  end = result.find('\}</pre></div></div><!--esi')

  result = result[start+12:end-30]

  return ({"text": result})

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


tools = [wikipedia_text_exporter]
prompt = hub.pull("hwchase17/react-chat")

os.environ["GROQ_API_KEY"] = "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"



llm = ChatGroq(model="llama3-8b-8192")

chat_history = ConversationBufferWindowMemory(k=10)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


user_input = input("Input")
invoke(user_input)
