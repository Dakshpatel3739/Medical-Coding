import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import gradio as gr
from retriever import retrieve_relevant_codes, get_code_from_gemini

# Function to process the user input
def process_input(query):
    # Retrieve relevant codes based on query
    retrieved_codes = retrieve_relevant_codes(query)
    
    # Get the predicted code from Gemini API
    predicted_code = get_code_from_gemini(query, retrieved_codes)
    
    return predicted_code

# Set up the Gradio interface
iface = gr.Interface(fn=process_input, inputs="text", outputs="text", 
                     title="Medical Code Prediction",
                     description="Enter a medical description (e.g., 'fever and headache') to get the predicted ICD/HCPCS code.")

# Launch the interface
iface.launch(share=True)
