import os
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

local_path = (
    os.getenv('MODEL_PATH')
)

# If you want to use a custom model add the backend parameter
# Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
llm = GPT4All(model=local_path, backend="gptj")

TEMPLATE = """
You are smart AI assistant. You will answer the question or perform the task in best possible way.
Do not try to complete the user question or add onto it, just answer it or perform the task.
Question/Task :{question}"""

prompt = PromptTemplate(template=TEMPLATE, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)


def llm_prompt(question):
    """Generates a response from model"""
    response = llm_chain.invoke({"question": question})
    print("AI Generated Response:", response["text"])
    return response["text"]


def get_llm_answer(text):
    """Cleans the question text and makes a call to get response from model"""
    # Clean the text by removing emojis and images
    clean_text = re.sub(r'<[^>]+>', '', text)  # Removes image URLs or any Slack-specific markup
    clean_text = re.sub(r':[^:]+:', '', clean_text)  # Removes Slack emojis
    # Replace double quotes with another symbol
    clean_text = re.sub(r'"([^"]*)"', r'<\1>', clean_text)
    return llm_prompt(question=clean_text)
