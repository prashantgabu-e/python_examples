from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
import os


os.environ["GROQ_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"
tools = [TavilySearchResults(max_results=1)]


from langchain_groq import ChatGroq

chat = ChatGroq(model="llama3-8b-8192")


from langchain_core.prompts import ChatPromptTemplate

# Adapted from https://smith.langchain.com/hub/jacob/tool-calling-agent
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
        ),
        ("placeholder", "{messages}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

from langchain.agents import AgentExecutor, create_tool_calling_agent

agent = create_tool_calling_agent(chat, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

from langchain_core.messages import HumanMessage

# result = agent_executor.invoke({"messages": [HumanMessage(content="I'm Nemo!")]})
# print(result)

from langchain_core.messages import AIMessage, HumanMessage

result = agent_executor.invoke(
    {
        "messages": [
            HumanMessage(content="I'm Nemo!"),
            AIMessage(content="Hello Nemo! How can I assist you today?"),
            HumanMessage(content="What is my name?"),
        ],
    }
)
print(result)