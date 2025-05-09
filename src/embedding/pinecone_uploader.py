from pinecone import Pinecone, ServerlessSpec
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()
# from src.constants.constant import *

pinecone_api=os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME='product-recommend'
# Initialize Pinecone
# pinecone.init(api_key=pinecone_api, environment='us-east-1')

# # Create or connect to an index
# index_name = PINECONE_INDEX_NAME
# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(index_name, dimension=1536)  # Dim of embeddings

# # Connect to the index
# index = pinecone.Index(index_name)

# # Load the embeddings and product data


# # Prepare data for insertion
# ids = [str(i) for i in range(len(embeddings_df))]
# embeddings = embeddings_df.values.tolist()
# metadata = product_data.to_dict(orient='records')

# # Insert the data into Pinecone
# batch_size = 100  # For efficient uploads
# for i in range(0, len(embeddings), batch_size):
#     index.upsert(
#         vectors=list(zip(ids[i:i+batch_size], embeddings[i:i+batch_size], metadata[i:i+batch_size]))
#     )

# print("Embeddings uploaded to Pinecone!")


# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api)

# Create or connect to an index
index_name = PINECONE_INDEX_NAME
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Dim of embeddings
        metric='cosine',  # You can choose the metric that fits your use case
        spec=ServerlessSpec(
            cloud='aws',  # Specify the cloud provider
            region='us-east-1'  # Specify the region
        )
    )

# Connect to the index
index = pc.Index(index_name)

# Load the embeddings and product data
embeddings_df = pd.read_csv('artifacts/embeddings/embeddings.csv')
product_data = pd.read_csv('artifacts/data/cleaned_data.csv')

# Prepare data for insertion
ids = [str(i) for i in range(len(embeddings_df))]
embeddings = embeddings_df.values.tolist()
metadata = product_data.to_dict(orient='records')

# Insert the data into Pinecone
batch_size = 100  # For efficient uploads
for i in range(0, len(embeddings), batch_size):
    index.upsert(
        vectors=list(zip(ids[i:i+batch_size], embeddings[i:i+batch_size], metadata[i:i+batch_size]))
    )

print("Embeddings uploaded to Pinecone!")
