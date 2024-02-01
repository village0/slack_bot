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

TEMPLATE = """Question :{question}
Answer: Answer only the question asked. Do not add extra questions or details to the answer."""

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
    clean_text = re.sub(r':[^:]+:', '', text)  # Removes Slack emojis
    clean_text = re.sub(r'<[^>]+>', '', clean_text)  # Removes image URLs or any Slack-specific markup
    return llm_prompt(question=clean_text)
