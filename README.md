# Welcome! 

This chatbot uses RAG to answer questions about the Seven Wonders of the Ancient World. 

Here are sample questions you can ask it:

1. What is the Great Pyramid of Giza?
2. What is the Hanging Gardens of Babylon?
3. What is the Temple of Artemis at Ephesus?
4. What is the Statue of Zeus at Olympia?
5. What is the Mausoleum at Halicarnassus?
6. Where is Gardens of Babylon?
7. Why did people build Great Pyramid of Giza?
8. What does Rhodes Statue look like?
9. Why did people visit the Temple of Artemis?
10. What is the importance of Colossus of Rhodes?
11. What happened to the Tomb of Mausolus?
12. How did Colossus of Rhodes collapse?

## How is it built?

### Poetry package management

This project uses [Poetry](https://python-poetry.org/) for package management.

It uses [this `pyproject.toml` file](pyproject.toml)

To install dependencies:

```bash
pip install poetry
poetry install
```

### Data source: 

The data is from the [Seven Wonders dataset][1] on Hugging Face. https://huggingface.co/datasets/bilgeyucel/seven-wonders

### Method

The chatbots retrieval mechanism is developed using Retrieval Augmented Generation (RAG) with [Haystack](https://haystack.deepset.ai/tutorials/22_pipeline_with_promptnode) and its user interface is built with [Chainlit](https://docs.chainlit.io/overview). It is using OpenAI GPT-3.5-turbo. 

### Pipeline steps (Haystack)

1. Initialize in-memory Document store

```python
# Initialize Haystack's QA system
document_store = InMemoryDocumentStore(use_bm25=True)
```
2. Load dataset from HF

```python
dataset = load_dataset("bilgeyucel/seven-wonders", split="train")
```

3. Transform documents and load into document store

```python
document_store.write_documents(dataset)
```
4. Initialize a RAG prompt

```
rag_prompt = PromptTemplate(
    prompt="""Synthesize a brief answer from the following text for the given question.
                             Provide a clear and concise response that summarizes the key points and information presented in the text.
                             Your answer should be in your own words and be no longer than 50 words.
                             \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
    output_parser=AnswerParser(),
)

```

5. Set the nodes using GPT-3.5-turbo

```python
 Set up nodes
retriever = BM25Retriever(document_store=document_store, top_k=2)
pn = PromptNode("gpt-3.5-turbo", 
                api_key=MY_API_KEY, 
                model_kwargs={"stream":False},
                default_prompt_template=rag_prompt)

```

6. Build the pipeline

```python
# Set up pipeline
pipe = Pipeline()
pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
pipe.add_node(component=pn, name="prompt_node", inputs=["retriever"])
```

### Connecting the pipeline to Chainlit

```python

@cl.on_message
async def main(message: str):
    # Use the pipeline to get a response
    output = pipe.run(query=message)

    # Create a Chainlit message with the response
    response = output['answers'][0].answer
    msg = cl.Message(content=response)

    # Send the message to the user
    await msg.send()
```

### Run application

``` bash
poetry run chainlit run src/app.py --port 7860
```