from haystack.nodes import WebRetriever
from haystack.schema import Document
from typing import List 
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import AnswerParser, PromptNode, PromptTemplate
from haystack import Pipeline
from haystack.nodes import  DensePassageRetriever
import os
from dotenv import load_dotenv

def initialize_documents(serp_key, nl_query):
    """
    Initialize documents retrieved from the SERP API.

    Args:
        serp_key (str): API key for the SERP API.
        nl_query (str): Natural language query to retrieve documents for.
        
    """
     # Initialize WebRetriever
    retriever = WebRetriever(api_key=serp_key, 
                            mode="preprocessed_documents",
                            top_k=100)

    # Retrieve documents based a natural language query
    documents : List[Document] = retriever.retrieve(query=nl_query)

    return documents

def initialize_faiss_document_store(documents):
    """
    Initialize a FAISS document store and retriever.

    Args:
        documents (List[Document]): List of documents to be stored in the document store.

    Returns:
        document_store (FAISSDocumentStore): FAISS document store.
        retriever (DensePassageRetriever): Dense passage retriever.
    """
    
    # Initialize document store
    document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", return_embedding=True)

    retriever = DensePassageRetriever(
                document_store=document_store,
                query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                use_gpu=True,
                embed_title=True,
    )

    # Delete existing documents in document store
    document_store.delete_documents()
    document_store.write_documents(documents)

    # Add documents embeddings to index
    document_store.update_embeddings(retriever=retriever)

    return document_store, retriever

def initialize_rag_pipeline(document_store, retriever, openai_key):
    """
    Initialize a pipeline for RAG-based question answering.

    Args:
        document_store (FAISSDocumentStore): FAISS document store.
        retriever (DensePassageRetriever): Dense passage retriever.
        openai_key (str): API key for OpenAI.

    Returns:
        query_pipeline (Pipeline): Pipeline for RAG-based question answering.
    """
    prompt_template = PromptTemplate(prompt = """"Answer the following query based on the provided context. If the context does
                                                not include an answer, reply with 'The data does not contain information related to the question'.\n
                                                Query: {query}\n
                                                Documents: {join(documents)}
                                                Answer: 
                                            """,
                                            output_parser=AnswerParser())
    prompt_node = PromptNode(model_name_or_path = "gpt-4",
                            api_key = openai_key,
                            default_prompt_template = prompt_template,
                            max_length = 500,
                            model_kwargs={"stream":True})

    query_pipeline = Pipeline()
    query_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    query_pipeline.add_node(component=prompt_node, name="PromptNode", inputs=["Retriever"])

    return query_pipeline

if __name__=="__main__":
    # Load environment variables (if any)
    load_dotenv("../.env")
    serp = os.getenv("SERP_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    # Initialize documents
    documents = initialize_documents(serp_key=serp, nl_query="IMDB movie reviews for the Barbie movie (2023)")

    # Initialize document store and retriever
    document_store, retriever = initialize_faiss_document_store(documents=documents)

    # Initialize pipeline
    query_pipeline = initialize_rag_pipeline(document_store=document_store, retriever=retriever, openai_key=openai_key)



