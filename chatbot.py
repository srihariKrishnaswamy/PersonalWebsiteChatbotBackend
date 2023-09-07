from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from dotenv import load_dotenv

load_dotenv()

BASE_PROMPT = "You are a chatbot Answering questions about me, Srihari Krishna. You've been trained on custom data about me, Srihari. Limit your responses to be under 50 words"

def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600
    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
    index.save_to_disk('index.json')
    return index

def ask_ai():
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    while True:
        Query = input("What do you want to ask? ")
        response = index.query(f"{BASE_PROMPT}\nUser Query: {Query}")
        print(f"Response: {response.response}")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
construct_index("context_data/data")
ask_ai()