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

### Data source: 

The data is from the [Seven Wonders dataset][1] on Hugging Face. https://huggingface.co/datasets/bilgeyucel/seven-wonders

### Method

The chatbots retrieval mechanism is developed using Retrieval Augmented Generation (RAG) with [Haystack](https://haystack.deepset.ai/tutorials/22_pipeline_with_promptnode) and its user interface is built with [Chainlit](https://docs.chainlit.io/overview). It is using OpenAI GPT-3.5-turbo. 