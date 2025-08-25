import re
import pandas as pd

# Function to extract ICD codes and descriptions
def extract_icd_codes(text):
    # Regular expression pattern to match ICD codes (e.g., A01, B21, etc.)
    icd_pattern = r"([A-Z]\d{2,3})(?:\s*-\s*|\s+)(.*?)(?=\n|$)"
    
    # Find all matching ICD codes and their descriptions
    matches = re.findall(icd_pattern, text)
    icd_codes = [{"code": match[0], "description": match[1]} for match in matches]
    
    return icd_codes

# Function to process the extraction from text files
def extract_from_text_files(icd_text_path, hcpcs_text_path):
    # Load the extracted text from files
    with open(icd_text_path, 'r') as icd_file:
        icd_text = icd_file.read()
        
    with open(hcpcs_text_path, 'r') as hcpcs_file:
        hcpcs_text = hcpcs_file.read()
    
    # Extract ICD codes and descriptions
    print("Extracting ICD codes from the ICD text file...")
    icd_codes = extract_icd_codes(icd_text)
    
    # Extract HCPCS codes and descriptions (similar to ICD extraction)
    print("Extracting HCPCS codes from the HCPCS text file...")
    hcpcs_codes = extract_icd_codes(hcpcs_text)  # You can create a different regex pattern for HCPCS if needed
    
    # Convert the extracted data to DataFrames
    df_icd = pd.DataFrame(icd_codes)
    df_hcpcs = pd.DataFrame(hcpcs_codes)
    
    # Save the results to CSV files
    df_icd.to_csv('output/icd_codes.csv', index=False)
    df_hcpcs.to_csv('output/hcpcs_codes.csv', index=False)
    
    print("Extraction complete! ICD and HCPCS codes saved to 'output/icd_codes.csv' and 'output/hcpcs_codes.csv'.")

# Paths for the extracted text files
icd_text_path = 'output/icd_extracted_text.txt'
hcpcs_text_path = 'output/hcpcs_extracted_text.txt'

# Run the extraction
extract_from_text_files(icd_text_path, hcpcs_text_path)
