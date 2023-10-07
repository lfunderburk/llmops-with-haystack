import chainlit as cl
from faissdenseretrieval import initialize_documents, initialize_faiss_document_store, initialize_rag_pipeline
import os
from dotenv import load_dotenv

# Load environment variables (if any)
load_dotenv("../.env")
serp = os.getenv("SERP_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize documents
documents = initialize_documents(serp_key=serp, nl_query="IMDB movie reviews for the Barbie movie (2023)")

# Initialize document store and retriever
document_store, retriever = initialize_faiss_document_store(documents=documents)

# Initialize pipeline
query_pipeline = initialize_rag_pipeline(retriever=retriever, openai_key=openai_key)

@cl.on_message
async def main(message: str):
    # Use the pipeline to get a response
    output = query_pipeline.run(query=message)

    # Create a Chainlit message with the response
    response = output['answers'][0].answer
    msg = cl.Message(content=response)

    # Send the message to the user
    await msg.send()
