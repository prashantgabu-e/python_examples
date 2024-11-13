from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from typing import List, Dict




os.environ["GROQ_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"


from langchain_groq import ChatGroq

llm = ChatGroq(model="llama3-8b-8192")



# Initialize Tavily search tool
search = TavilySearchResults(
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

# Create a custom tool for getting the current date
@tool
def get_current_date():
    """Returns the current date. Use this when you need to know today's date."""
    from datetime import date
    return date.today().strftime("%Y-%m-%d")

# List of tools
tools = [
    search,
    get_current_date
]

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant. You have access to tools that can help you provide better answers:
    - A search tool to find current information
    - A tool to get the current date
    
    Use these tools only when necessary. For general knowledge questions or when you're confident in your response,
    you don't need to use tools. Use tools when:
    1. You need current information
    2. You need to verify facts
    3. You need the current date
    
    Always be direct and concise in your responses."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

class Chatbot:
    def __init__(self):
        self.chat_history = []
        
    def process_message(self, user_input: str) -> str:
        """
        Process a single message from the user and return the response.
        
        Args:
            user_input (str): The user's message
            
        Returns:
            str: The assistant's response
        """
        # Add the new message to chat history
        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": self.chat_history
        })
        print(response)
        
        # Update chat history
        self.chat_history.extend([
            ("human", user_input),
            ("assistant", response["output"])
        ])
        
        return response

# Example usage
if __name__ == "__main__":
    chatbot = Chatbot()
    
    # Example conversation
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        try:
            response = chatbot.process_message(user_input)
            print("\nAssistant:", response)
        except Exception as e:
            print(f"An error occurred: {e}")