from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file


# Define a very simple tool function that returns the current time
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime  # Import datetime module to get current time

    now = datetime.datetime.now()  # Get current time
    return now.strftime("%I:%M %p")  # Format time in H:MM AM/PM format
tools = [
    Tool(
        name="Time",  # Name of the tool
        func=get_current_time,  # Function that the tool will execute
        # Description of the tool
        description="Useful for when you need to know the current time",
    ),
]
import getpass
import os

os.environ["GROQ_API_KEY"] = "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"

from langchain_groq import ChatGroq

llm = ChatGroq(model="llama3-8b-8192")

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True,
)

# Create an agent executor from the agent and tools
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

response = agent_executor.invoke({"input": "What is moon?"})


print("response:", response)


# print(llm)

# llm_with_tools = llm.bind_tools(tools)
# # print(llm_with_tools)
# query = "What is moon?"

# result = llm_with_tools.invoke(query)
# print(result)