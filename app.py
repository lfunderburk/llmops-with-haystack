import torch
torch.device('cpu')

# Imports and Initializations for Chainlit
import chainlit as cl
from dotenv import load_dotenv

# Imports and Initializations for Haystack
from haystack.document_stores import InMemoryDocumentStore
from datasets import load_dataset
from haystack.nodes import BM25Retriever, PromptTemplate, AnswerParser, PromptNode
import os
from haystack.pipelines import Pipeline

# Load environment variables (if any)
load_dotenv(".env")
load_dotenv()
MY_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Haystack's QA system
document_store = InMemoryDocumentStore(use_bm25=True)
dataset = load_dataset("bilgeyucel/seven-wonders", split="train")
document_store.write_documents(dataset)


rag_prompt = PromptTemplate(
    prompt="""Synthesize a brief answer from the following text for the given question.
                             Provide a clear and concise response that summarizes the key points and information presented in the text.
                             Your answer should be in your own words and be no longer than 50 words.
                             \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
    output_parser=AnswerParser(),
)

# Set up nodes
retriever = BM25Retriever(document_store=document_store, top_k=2)
pn = PromptNode("gpt-3.5-turbo", 
                api_key=MY_API_KEY, 
                model_kwargs={"stream":False},
                default_prompt_template=rag_prompt)

# Set up pipeline
pipe = Pipeline()
pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
pipe.add_node(component=pn, name="prompt_node", inputs=["retriever"])

@cl.on_message
async def main(message: str):
    # Use the pipeline to get a response
    output = pipe.run(query=message)

    # Create a Chainlit message with the response
    response = output['answers'][0].answer
    msg = cl.Message(content=response)

    # Send the message to the user
    await msg.send()

if __name__ == "__main__":
    # You can add any Chainlit app initialization or run code here
    pass
