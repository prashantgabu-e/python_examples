import requests
from langchain import LLMChain, OpenAI, Tool, AgentExecutor
from langchain.agents import load_tools, initialize_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Step 1: Set up LLM
llm = OpenAI(model_name="gpt-4")

# Step 2: Tavily Search Tool Implementation
def tavily_search(query: str) -> str:
    # Replace with actual Tavily API call
    url = "TAVILY_API_ENDPOINT"
    headers = {
        "Authorization": f"Bearer YOUR_TAVILY_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {"query": query}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json()
        return results.get("data", "No results found.")
    except requests.exceptions.RequestException as e:
        return f"Error occurred during Tavily search: {e}"

# Define the Tavily tool
tavily_tool = Tool(
    name="Tavily Search",
    func=tavily_search,
    description="Performs a search using Tavily to retrieve external information."
)

# Step 3: Create the Prompt Template
prompt_template = """
You are an AI assistant. You will answer questions directly or use Tavily Search if the input needs it.
If unsure about something, call Tavily Search for additional information.

User input: {input}
"""

# Initialize prompt template and conversation memory
prompt = PromptTemplate(input_variables=["input"], template=prompt_template)
memory = ConversationBufferMemory(memory_key="chat_history")

# Step 4: Set up LangChain agent with Tavily tool
tools = load_tools(["openai"], tool_list=[tavily_tool])

# Load the agent with the LLM, tools, and template
agent_chain = LLMChain(prompt=prompt, llm=llm)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True,
    memory=memory
)

# Step 5: Function to Run the Chatbot with Conditional Tool Usage
def chat_with_bot(user_input: str):
    response = agent({"input": user_input})
    return response['output']

# Example Usage
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        bot_response = chat_with_bot(user_input)
        print(f"Bot: {bot_response}")
