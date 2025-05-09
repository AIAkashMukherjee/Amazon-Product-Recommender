# src/retriever.py

from pinecone import Pinecone
import pandas as pd
from typing import List
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
# Load .env for Pinecone keys
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENVIRONMENT = "gcp-starter"  # e.g., "gcp-starter"   
PINECONE_INDEX_NAME = 'product-recommend'

class ProductRetriever:
    def __init__(self,  pinecone_api_key: str = PINECONE_API_KEY, 
                 index_name: str = PINECONE_INDEX_NAME,  embedding_model_name: str = "all-MiniLM-L6-v2"):
        # Initialize Pinecone
        # pinecone.init(api_key=pinecone_api_key)
        # self.index = pinecone.Index(index_name)
        
        # # Load embedding model
        # self.embedder = SentenceTransformer(embedding_model_name)

        self.pinecone = Pinecone(api_key=pinecone_api_key)
        self.index = self.pinecone.Index(index_name)
        
        # Load embedding model
        self.embedder = SentenceTransformer(embedding_model_name)

    def embed_query(self, query: str) -> List[float]:
        return self.embedder.encode(query,convert_to_numpy=True).tolist()

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        # Generate query embedding
        query_embedding = self.embed_query(query)

        # Query Pinecone index
        results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

        # Format and return results
        retrieved_products = []
        for match in results['matches']:
            product_info = {
                "id": match['id'],
                "score": match['score'],
                "title": match['metadata'].get('title', ''),
                "category": match['metadata'].get('category', ''),
                "availability": match['metadata'].get('availability', ''),
                "price": match['metadata'].get('price', ''),
                "rating": match['metadata'].get('rating', ''),
                "reviews": match['metadata'].get('reviews', '')
            }
            retrieved_products.append(product_info)

        return retrieved_products


def retrieve_similar_products(user_query: str, top_k: int = 5) -> List[dict]:
    retriever = ProductRetriever()
    return retriever.search(user_query, top_k=top_k)


if __name__ == "__main__":
    query = "Looking for a gaming laptop with high refresh rate"
    results = retrieve_similar_products(query, top_k=5)
    
    print("\n=== Retrieved Products ===")
    for prod in results:
        print(f"- {prod['title']} (₹{prod['price']}, ⭐ {prod['rating']})")