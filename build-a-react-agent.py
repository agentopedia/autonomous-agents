from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import load_tools
import os
os.environ["WOLFRAM_ALPHA_APPID"] = "" # Visit https://products.wolframalpha.com/api to get the key
os.environ["OPENAI_API_KEY"] = "" #Visit https://platform.openai.com 
llm = OpenAI(temperature=0)
from langchain.agents import load_tools
tools = load_tools(["wolfram-alpha"])
zero_shot_agent = initialize_agent(agent="zero-shot-react-description", tools=tools, llm=llm,  verbose=True, max_iterations=3)
output = zero_shot_agent("what is (4.5*2.1)^2.2?")
print (output)
