# embedding_generator.py

import os
import sys
import requests
import pandas as pd
import numpy as np
# from openai import OpenAI
from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
from tqdm import tqdm
# Load pre-trained model and tokenizer

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')


# Function to encode text
# def get_embeddings(texts):
#     inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
#     with torch.no_grad():
#         embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Mean pooling
#     return embeddings.numpy()

def get_embeddings(texts, batch_size=32):
    """
    Generate embeddings for a list of texts using mean pooling.
    """
    embeddings_list = []

    for i in tqdm(range(0, len(texts), batch_size), desc="Generating embeddings"):
        batch_texts = texts[i:i+batch_size]
        inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)  # Mean pooling
            embeddings_list.append(embeddings.cpu().numpy())

    all_embeddings = np.vstack(embeddings_list)
    return all_embeddings

# Load your clean data
data = pd.read_csv('artifacts/data/cleaned_data.csv')

# Extract titles or other fields for embedding
titles = data['title'].fillna('').tolist()

# Generate embeddings for the titles
embeddings = get_embeddings(titles)

# Save the embeddings as a numpy array or pandas DataFrame
os.makedirs('artifacts/embeddings',exist_ok=True)
embeddings_df = pd.DataFrame(embeddings)

embeddings_df.to_csv('artifacts/embeddings/embeddings.csv', index=False)
