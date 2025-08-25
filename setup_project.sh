#!/bin/bash

# Set project name
PROJECT_NAME="medical-code-prediction"

# Create the root directory for the project
mkdir $PROJECT_NAME
cd $PROJECT_NAME

# Create necessary subdirectories
mkdir -p data output logs src models

# Create a README.md
cat <<EOF > README.md
# Medical Code Prediction using RAG Architecture

## Project Overview

This project aims to develop a **Medical Code Prediction Model** using the **Retrieval-Augmented Generation (RAG)** approach. The system will predict ICD/HCPCS codes based on medical descriptions using embeddings, **Gemini Pro API**, and **Gradio** interface. The model will be deployed on **Lightning AI** for scalability.

---

## Folder Structure

- `data/`: Contains the input raw PDF files and any extracted text.
- `src/`: All the source code, including PDF extraction, embeddings, retrieval, API integration, and Gradio interface.
- `models/`: Placeholder for the trained model.
- `output/`: Output files like extracted ICD codes and logs.
- `requirements.txt`: Required libraries for the project.
- `config.yaml`: Configuration file for API keys and other settings.
- `Dockerfile`: For containerization of the application.

---

## Installation

### Step 1: Clone the repository

\`\`\`bash
git clone https://github.com/yourusername/medical-code-prediction.git
cd medical-code-prediction
\`\`\`

### Step 2: Install dependencies

Make sure you have Python 3.8+ installed. Then, run:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 3: Set up configuration

Create a \`config.yaml\` file and fill in the necessary fields (e.g., Gemini API key).

\`\`\`yaml
gemini_api_key: "YOUR_GEMINI_API_KEY"
\`\`\`

---

## Usage

### Step 1: Extract ICD/HCPCS Codes from PDFs

To extract ICD codes from a PDF, run:

\`\`\`bash
python src/pdf_extraction.py --pdf_path data/ICD_HCPCS_example.pdf
\`\`\`

This will generate a \`icd_codes.csv\` file in the \`output/\` directory.

### Step 2: Run the Gradio Interface

Once the extraction is done, you can start the Gradio interface to interact with the model:

\`\`\`bash
python src/gradio_interface.py
\`\`\`

---

## Configuration

You can adjust settings such as the number of retrieved chunks or fine-tune the Gemini API integration by editing \`config.yaml\`.

---

## Docker Support

To run the application in a Docker container, build the Docker image:

\`\`\`bash
docker build -t medical-code-prediction .
\`\`\`

And run it:

\`\`\`bash
docker run -p 7860:7860 medical-code-prediction
\`\`\`

This will expose the Gradio interface at \`http://localhost:7860\`.

---

## Notes

- **Gemini API**: You’ll need a Gemini API key, which you can include in the \`config.yaml\` file.
- **Deployment**: For production deployments, consider using **Lightning AI** or **Heroku**.

---

## License

This project is licensed under the MIT License.
EOF

# Create requirements.txt
cat <<EOF > requirements.txt
pandas==1.5.3
PyMuPDF==1.19.6
pdfplumber==0.5.28
sentence-transformers==2.2.0
faiss-cpu==1.7.2
requests==2.28.1
gradio==3.4.4
torch==1.13.1
EOF

# Create config.yaml
cat <<EOF > config.yaml
gemini_api_key: "YOUR_GEMINI_API_KEY"
embedding_model: "all-MiniLM-L6-v2"  # Sentence Transformer model
faiss_index_path: "faiss.index"  # FAISS index path (if using FAISS)
EOF

# Create Dockerfile
cat <<EOF > Dockerfile
# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Gradio interface port
EXPOSE 7860

# Run the Gradio interface by default
CMD ["python", "src/gradio_interface.py"]
EOF

# Create the initial Python scripts (you can fill in the logic later)

# src/pdf_extraction.py
cat <<EOF > src/pdf_extraction.py
import fitz  # PyMuPDF
import pdfplumber

def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def extract_text_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

if __name__ == "__main__":
    pdf_path = 'data/ICD_HCPCS_example.pdf'
    extracted_text = extract_text_pymupdf(pdf_path)  # You can also use pdfplumber
    with open('output/extracted_text.txt', 'w') as f:
        f.write(extracted_text)
EOF

# src/icd_code_extraction.py
cat <<EOF > src/icd_code_extraction.py
import re
import pandas as pd

def extract_icd_codes(text):
    icd_pattern = r"([A-Z]\d{2,3})(?:\s*-\s*|\s+)(.*?)(?=\n|$)"
    matches = re.findall(icd_pattern, text)
    icd_codes = [{"code": match[0], "description": match[1]} for match in matches]
    return icd_codes

if __name__ == "__main__":
    with open('output/extracted_text.txt', 'r') as file:
        extracted_text = file.read()
    icd_codes = extract_icd_codes(extracted_text)
    df_icd = pd.DataFrame(icd_codes)
    df_icd.to_csv('output/icd_codes.csv', index=False)
EOF

# src/gradio_interface.py
cat <<EOF > src/gradio_interface.py
import gradio as gr
import requests
from config import gemini_api_key

def get_icd_code(description):
    api_url = "https://api.gemini.com/v1/predict"
    headers = {"Authorization": f"Bearer {gemini_api_key}"}
    payload = {
        "prompt": f"Generate ICD code for: {description}",
        "max_tokens": 100
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()['choices'][0]['text']

iface = gr.Interface(fn=get_icd_code, inputs="text", outputs="text")
iface.launch()
EOF

# Make sure the src directory is initialized as a Python package
touch src/__init__.py

echo "Project structure has been set up successfully!"
