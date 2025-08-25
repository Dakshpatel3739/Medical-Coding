import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import requests
from config import gemini_api_key

# Load the FAISS index and sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('output/faiss.index')

# Load the ICD and HCPCS data
df_icd = pd.read_csv('output/icd_codes.csv')
df_hcpcs = pd.read_csv('output/hcpcs_codes.csv')

# Function to retrieve the top-k relevant codes from FAISS index
def retrieve_relevant_codes(query, top_k=5):
    # Generate embedding for the query
    query_embedding = model.encode([query])

    # Search the FAISS index for the most similar descriptions
    D, I = index.search(np.array(query_embedding).astype('float32'), top_k)

    # Retrieve the top_k most relevant ICD/HCPCS codes and their descriptions
    retrieved_codes = []
    for i in range(top_k):
        if I[0][i] < len(df_icd):  # ICD code
            code = df_icd.iloc[I[0][i]]['code']
            description = df_icd.iloc[I[0][i]]['description']
        else:  # HCPCS code
            idx = I[0][i] - len(df_icd)  # Adjust index for HCPCS
            code = df_hcpcs.iloc[idx]['code']
            description = df_hcpcs.iloc[idx]['description']

        retrieved_codes.append({"code": code, "description": description, "similarity": D[0][i]})

    return retrieved_codes

# Function to call Gemini Pro API to predict the code based on context
def get_code_from_gemini(description, retrieved_codes):
    context = " ".join([f"Code: {r['code']}, Description: {r['description']}" for r in retrieved_codes])
    prompt = f"Given the following context, predict the code for the description: '{description}'.\n\nContext: {context}"

    # Correct Gemini Pro API URL
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": gemini_api_key
    }

    # Payload for the API request
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Make the POST request to Gemini API
    response = requests.post(api_url, json=payload, headers=headers)

    # Print the full API response for debugging
    print("API Response:", response.json())

    # Ensure the API response contains the expected 'candidates' key
    if 'candidates' in response.json():
        predicted_code = response.json()['candidates'][0]['content']['parts'][0]['text']
        return predicted_code.strip()
    else:
        print("Error: 'candidates' key not found in the API response.")
        return None

# Test the retrieval and Gemini integration
if __name__ == "__main__":
    query = "fever and headache"
    print(f"Query: {query}")

    # Retrieve relevant codes
    retrieved_codes = retrieve_relevant_codes(query)
    print("Retrieved codes:")
    for code in retrieved_codes:
        print(f"Code: {code['code']}, Description: {code['description']}, Similarity: {code['similarity']}")

    # Get the predicted code using Gemini
    predicted_code = get_code_from_gemini(query, retrieved_codes)
    if predicted_code:
        print(f"Predicted Code: {predicted_code}")
    else:
        print("Could not retrieve a predicted code.")
