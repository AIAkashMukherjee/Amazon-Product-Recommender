from dotenv import load_dotenv
import os
load_dotenv()

open_ai_api=os.getenv('OPENAI_API_KEY')
pinecone_api=os.getenv('PINECONE_API_KEY')
groq_api_key=os.getenv('GROQ_API_KEY')
PINECONE_INDEX_NAME='product-recommend'
DEFAULT_OPENAI_MODEL = "gpt-4"