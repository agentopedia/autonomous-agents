from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import load_tools
#load_tools is a function that loads the necessary tools for the agent.
import os
os.environ["WOLFRAM_ALPHA_APPID"] = "" # Visit https://products.wolframalpha.com/api to get the key
os.environ["OPENAI_API_KEY"] = "" #Visit https://platform.openai.com 
llm = OpenAI(temperature=0)
#Base LLM used for the agent is the OpenAI's GPT3.5 model
tools = load_tools(["wolfram-alpha"])
#In this case, the tool being loaded is "wolfram-alpha", which will be used to handle mathematical queries
zero_shot_agent = initialize_agent(agent="zero-shot-react-description", tools=tools, llm=llm,  verbose=True, max_iterations=3) 
#initialize_agent sets up an AI agent with the specified configuration.
#agent="zero-shot-react-description" specifies the type of agent to initialize.
#tools=tools provides the tools (in this case, Wolfram Alpha) that the agent will use.
#llm=llm assigns the OpenAI language model instance to the agent.
#verbose=True enables detailed logging of the agent's actions and decisions.
#max_iterations=3 limits the agent to a maximum of 3 iterations to complete the task.
output = zero_shot_agent("what is (4.5*2.1)^2.2?")
print (output)
