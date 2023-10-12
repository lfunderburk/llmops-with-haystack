from haystack.nodes import LinkContentFetcher
from haystack.schema import Document
from typing import List 
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import AnswerParser, PromptNode, PromptTemplate
from haystack import Pipeline
from haystack.nodes import  DensePassageRetriever
import os
from dotenv import load_dotenv

def initialize_faiss_document_store():
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

    return document_store, retriever

def fetch_web_content_from_list(link_list: List[str], retriever, document_store):
    """
    Fetch web content from a list of links.

    Args:
        link_list (List[str]): List of links.
    
    Returns:
        documents (List[Document]): List of documents.
    """

    link_content_fetcher = LinkContentFetcher()
    documents = []
    all_documents = []

    for link in link_list:
        documents : List[Document] = link_content_fetcher.fetch(url=link)
        document_store.write_documents(documents)
        all_documents.append(documents)

    document_store.delete_documents()
    document_store.write_documents(documents)

    # Add documents embeddings to index
    document_store.update_embeddings(retriever=retriever, batch_size = 2000)

    return all_documents


def initialize_rag_pipeline(retriever, openai_key):
    """
    Initialize a pipeline for RAG-based question answering.

    Args:
        retriever (DensePassageRetriever): Dense passage retriever.
        openai_key (str): API key for OpenAI.

    Returns:
        query_pipeline (Pipeline): Pipeline for RAG-based question answering.
    """
    prompt_template = PromptTemplate(prompt = """"Answer the following query based on the provided context. \
                                                Please include the relevant link or links that you used to answer the question. \
                                                If the context does
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

    load_dotenv("../.env")
    openai_key = os.getenv("OPENAI_API_KEY")

    links = ["https://www.gracedupage.org/about-us",
                'https://www.gracedupage.org/who-is-jesus',
                'https://www.gracedupage.org/purpose',
                'https://www.gracedupage.org/history',
                'https://www.gracedupage.org/pastoral-ministries',
                'https://www.gracedupage.org/leadership',
                'https://www.gracedupage.org/baptism-and-membership']

    document_store, retriever = initialize_faiss_document_store()

    documents = fetch_web_content_from_list(link_list=links, retriever=retriever, document_store=document_store)

    pipeline = initialize_rag_pipeline(retriever=retriever, openai_key=openai_key)
    answer = pipeline.run(query="What is the purpose of Grace Church?", documents=documents)

    print(answer)
