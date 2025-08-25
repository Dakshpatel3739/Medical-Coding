import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load ICD and HCPCS code data
df_icd = pd.read_csv('output/icd_codes.csv')
df_hcpcs = pd.read_csv('output/hcpcs_codes.csv')

# Function to create embeddings for ICD/HCPCS descriptions
def create_embeddings(df, column_name='description'):
    # Generate embeddings for the descriptions
    embeddings = model.encode(df[column_name].tolist(), show_progress_bar=True)
    return embeddings

# Create embeddings for ICD and HCPCS descriptions
print("Creating embeddings for ICD codes...")
icd_embeddings = create_embeddings(df_icd)

print("Creating embeddings for HCPCS codes...")
hcpcs_embeddings = create_embeddings(df_hcpcs)

# Combine the ICD and HCPCS embeddings into one set for retrieval
all_embeddings = np.vstack([icd_embeddings, hcpcs_embeddings])

# Initialize FAISS index for similarity search (L2 distance)
dim = all_embeddings.shape[1]
index = faiss.IndexFlatL2(dim)

# Add the embeddings to the FAISS index
index.add(all_embeddings)

# Save the FAISS index and embeddings for later use
faiss.write_index(index, 'output/faiss.index')
np.save('output/embeddings.npy', all_embeddings)

print("Embeddings and FAISS index saved!")
