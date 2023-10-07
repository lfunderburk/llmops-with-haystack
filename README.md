# Building RAG chatbots with Haystack

In this repository I explore the development of RAG (retrival augmented generation) pipelines, whose job is to give a Large Language Model like OpenAI's GPT-4 access to a corpus of documents, usually in a database or in-memory, so that it can answer questions about it. 

## In-memory chatbot

This chatbot uses RAG to answer questions about the Seven Wonders of the Ancient World.

[Read more here](first-rag-bot/chainlit-app/README.md)

## Retrieval QA chatbot from web scraping using FAISS

This chatbot can help you identify what people think about the Barbie (2023) movie. You can also ask it information about the movie.

[Read more here](retrieval-qa/README.md)