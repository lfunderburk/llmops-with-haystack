# What do people think about the Barbie (2023) movie?

This chatbot can help you identify what people think about the Barbie (2023) movie. You can also ask it information about the movie. 

### How it is built:

The application uses Haystack's WebRetriever class to scrape reviews from the internet. It uses a simple NLP query: "IMDB movie reviews for the Barbie movie (2023)" and 100 top k results were fetched.  The results were then stored into a FAISS document store. 

To retrieve answers I used the DensePassageRetriever class from Haystack using the following models:


query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",


The embeddings were applied onto the documents in the document store.

I then initialized a Haystack pipeline whose nodes include a prompt node that uses OpenAI's GPT-4 and the DensePassageRetriever node. Its user interface was built using Chainlit.

### How does it work?

1. The WebRetriever will scrape the internet for reviews of the Barbie movie (2023) based on the natural language query using the SERP API.
2. The WebRetriever transforms the results into Document objects which can then be saved into a FAISS document store.
3. The DensePassageRetriever` node will apply embeddings to the documents in the document store and then it will use the embeddings to retrieve the top k results for a given query.
4. When a user asks a question, the PromptNode will use the top k results to generate an answer using OpenAI's GPT-4.
