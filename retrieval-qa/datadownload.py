import os
from dotenv import load_dotenv

# Load environment variables (if any)
load_dotenv("../.env")
openaikey = os.getenv("OPENAI_API_KEY")
pinecone = os.getenv("PINECONE_API_KEY")