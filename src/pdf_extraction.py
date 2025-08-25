import fitz  # PyMuPDF
import pdfplumber
import os

# Function to extract text using PyMuPDF (fitz)
def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

# Function to extract text using pdfplumber
def extract_text_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to process the extraction for both ICD and HCPCS PDFs
def extract_from_pdfs(icd_pdf_path, hcpcs_pdf_path):
    # Ensure the output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')

    # Extract text from ICD and HCPCS PDFs
    print("Extracting text from ICD PDF...")
    icd_text = extract_text_pymupdf(icd_pdf_path)  # You can also use pdfplumber
    print("Extracting text from HCPCS PDF...")
    hcpcs_text = extract_text_pymupdf(hcpcs_pdf_path)  # You can also use pdfplumber

    # Save the extracted text to respective files
    with open('output/icd_extracted_text.txt', 'w') as icd_file:
        icd_file.write(icd_text)

    with open('output/hcpcs_extracted_text.txt', 'w') as hcpcs_file:
        hcpcs_file.write(hcpcs_text)

    print("Text extraction complete for both ICD and HCPCS!")

# Paths for the PDFs
icd_pdf_path = '/teamspace/studios/this_studio/medical-code-prediction/data/ICD.pdf'
hcpcs_pdf_path = '/teamspace/studios/this_studio/medical-code-prediction/data/HCPCS.pdf'

# Run the extraction
extract_from_pdfs(icd_pdf_path, hcpcs_pdf_path)
