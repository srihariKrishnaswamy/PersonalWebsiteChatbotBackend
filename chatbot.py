from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from dotenv import load_dotenv

load_dotenv()

BASE_PROMPT = "You are a chatbot answering questions about me, Srihari Krishna. You've been trained on custom data about me, Srihari. Limit your responses to 0-2 sentences. You should jump directly into the answer, do not preface it with \'Answer:\'"
filename = "index.json"


def create_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
    index.save_to_disk(filename)
    return index

def ask_chatbot(user_input):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    if not os.path.exists(filename):
        create_index("context_data/data")
    index = GPTSimpleVectorIndex.load_from_disk(filename)
    # user_input = input("What do you want to ask? ")
    res = index.query(f"{BASE_PROMPT}\nUser Query: {user_input}")
    return res.response

if __name__ == "__main__":
    print(ask_chatbot("Dummy input"))