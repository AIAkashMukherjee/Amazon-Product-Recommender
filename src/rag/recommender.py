import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dotenv import load_dotenv
from src.rag.retrieval import retrieve_similar_products

# Load environment variables
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Get Groq API Key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Ensure Groq API Key is available
if not GROQ_API_KEY:
    raise ValueError("Groq API key is required but not found in environment variables.")

# Import Groq client and set up
import openai
openai.api_key = GROQ_API_KEY
openai.api_base = "https://api.groq.com/openai/v1"  # Groq API endpoint
client = openai
model = "Llama-3.3-70b-Versatile"  # Groq Llama model

def generate_recommendation(user_query, retrieved_products, no_of_products=5):
    """Use Groq Llama model to generate recommendations"""
    
    # Format retrieved products into text
    products_text = ""
    for i, prod in enumerate(retrieved_products, 1):
        products_text += f"{i}. {prod['title']} (Price: ₹{prod['price']}, Rating: {prod['rating']}/5)\n"

    prompt = f"""
    You are an intelligent Amazon product recommender. 
    A user asked: "{user_query}"

    Here are some matching products:
    {products_text}

    Recommend the best "{no_of_products}" products from above and explain why they suit the user's needs in simple terms.
    Give your answer in this format:
    - Product 1: [Title]. Reason: ...
    - Product 2: [Title]. Reason: ...
    - Product 3: [Title]. Reason: ...
    """

    # Generate recommendation using Groq API
    response = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()

def recommend_products(user_query, top_k=5):
    """Main function: retrieve similar products and generate recommendation"""
    
    # Step 1: Retrieve similar products
    retrieved_products = retrieve_similar_products(user_query, top_k=top_k)

    # Step 2: Generate recommendation text using Groq model
    recommendation = generate_recommendation(user_query, retrieved_products, no_of_products=top_k)

    return {
        "user_query": user_query,
        "retrieved_products": retrieved_products,
        "recommendation": recommendation
    }

