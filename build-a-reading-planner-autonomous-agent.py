# Step 1: Install Required Libraries
# You need to install the required libraries before running the script.
# Use the following command to install the necessary packages.
# Note: These installations need to be run in your command-line interface, not within the script.

# pip install openai tavily-python langchain_community langchain_core langchain_openai

# Step 2: Set Up Environment Variables
# Here, we set up the API keys for Tavily and OpenAI. You must replace the placeholders with your actual API keys.
# Visit the respective websites to obtain these keys.

import os

os.environ['TAVILY_API_KEY'] = 'your_tavily_api_key_here'  # Visit https://tavily.com/#api to get a key
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'  # Visit https://platform.openai.com to get a key

# Step 3: Initialize Tavily Client
# Initialize the Tavily client with your API key to interact with the Tavily service.

from tavily import TavilyClient

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# Step 4: Set Up Tavily Search API Retriever
# This module allows us to perform searches using Tavily's API. We configure it to return a maximum of 3 results per query.

from langchain_community.retrievers import TavilySearchAPIRetriever

retriever = TavilySearchAPIRetriever(k=3)

# Example Query with the Tavily Retriever
query = "what year was breath of the wild released?"
retriever.invoke(query)

# Step 5: Define Output Parsers and Prompt Templates
# These modules handle the processing of output and define the prompts to interact with the OpenAI model.

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# Create a prompt template to answer questions based on provided context
prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

# Initialize the OpenAI model with a specific version
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Helper function to format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define a processing chain
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Example usage of the chain to answer a question
chain.invoke("Who is the prime minister of Brunei?")

# Step 6: Configure Google Generative AI
# We configure Google Generative AI using its API key for further generation tasks.

import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = 'your_google_api_key_here'  # Replace with your actual Google API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Set up generation configuration and safety settings
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_instruction = (
    "You are a highly accomplished teacher who understands the needs of various students and "
    "can build detailed well-planned reading plans for any complex topic by breaking them down "
    "into simple digestible nuggets."
)

model_gen = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    system_instruction=system_instruction,
    safety_settings=safety_settings
)

# Step 7: Define Helper Functions
# A helper function that generates a response using the configured model.

def model_response(text):
    response = model_gen.generate_content(text)
    return response.text

# Test the function with a simple prompt
model_response('Who are you?')

# Step 8: Generate a Learning Plan
# Function to generate a learning plan for a specified topic

def generate_reading_plan(topic):
    plan = model_response(f'''
        Imagine you are an expert on the {topic}. Generate a detailed reading plan consisting of 5 steps that will help the user master the topic.
        Output should contain the steps in the format of a list. Do not output anything else apart from the list. The steps should be restricted to a single line.
        Output:
        [Step 1; Step 2; Step 3; Step 4; Step 5]
    ''')
    return plan

# Example: Generate a reading plan for 'India'
print(generate_reading_plan('India'))

# Step 9: Execute and Track the Learning Plan
# We create an autonomous loop that goes through each step of the plan, executes it, and tracks the progress.

plan = generate_reading_plan('India')
steps = plan.split(';')
reading_plan = {}
memory_state = ""

for step in steps:
    print(step)
    step_response = model_response(f'''
        Execute the {step} within the context of the overall plan: {plan}, considering the progress made up to this point. 
        The following is the current state of the plan, summarizing key developments and decisions: {memory_state}. 
        Use this information to elaborate on how {step} fits into the broader objectives and any next actions that should be taken
    ''')
    reading_plan[step] = step_response
    memory_state = model_response(f'''
        Analyze the {reading_plan} and come up with the SPR. Below are the instructions.
        # MISSION
        You are a Sparse Priming Representation (SPR) writer. An SPR is a particular kind of use of language for advanced NLP, NLU, and NLG tasks, particularly useful for the latest generation Large Language Models (LLMs). You will be given information by the USER which you are to render as an SPR.

        # THEORY
        LLMs are a kind of deep neural network. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind. These are called latent abilities and latent content, collectively referred to as latent space. The latent space of a LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network. This is not unlike how the right shorthand cues can prime a human mind to think in a certain way. Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way.

        # METHODOLOGY
        Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human.
    ''')

# Final Output: Display the Final Reading Plan
final_plan = model_response(f'''Generate a detailed reading plan based on the context provided {reading_plan}''')
print(final_plan)
