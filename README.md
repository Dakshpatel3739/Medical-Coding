# Medical Code Prediction using RAG Architecture

## Project Overview

This project aims to develop a **Medical Code Prediction Model** using the **Retrieval-Augmented Generation (RAG)** approach. The system will predict ICD/HCPCS codes based on medical descriptions using embeddings, **Gemini Pro API**, and **Gradio** interface. The model will be deployed on **Lightning AI** for scalability.

---

## Folder Structure

-  Contains the input raw PDF files and any extracted text.
-  All the source code, including PDF extraction, embeddings, retrieval, API integration, and Gradio interface.
-  Placeholder for the trained model.
-  Output files like extracted ICD codes and logs.
-  Required libraries for the project.
-  Configuration file for API keys and other settings.
-  For containerization of the application.

---

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/Dakshpatel3739/Medical-Coding.git
cd medical-code-prediction
```

### Step 2: Install dependencies

Make sure you have Python 3.8+ installed. Then, run:

```bash
pip install -r requirements.txt
```

### Step 3: Set up configuration

Create a `config.yaml` file and fill in the necessary fields (e.g., Gemini API key).

```yaml
gemini_api_key: "YOUR_GEMINI_API_KEY"
```

---

## Usage

### Step 1: Extract ICD/HCPCS Codes from PDFs

To extract ICD codes from a PDF, run:

```bash
python src/pdf_extraction.py --pdf_path data/ICD_HCPCS_example.pdf
```

This will generate a `icd_codes.csv` file in the `output/` directory.

### Step 2: Run the Gradio Interface

Once the extraction is done, you can start the Gradio interface to interact with the model:

```bash
python src/gradio_interface.py
```

---

## Configuration

You can adjust settings such as the number of retrieved chunks or fine-tune the Gemini API integration by editing `config.yaml`.

---

## Docker Support

To run the application in a Docker container, build the Docker image:

```bash
docker build -t medical-code-prediction .
```

And run it:

```bash
docker run -p 7860:7860 medical-code-prediction
```

This will expose the Gradio interface at `http://localhost:7860`.

---

## Notes

- **Gemini API**: You’ll need a Gemini API key, which you can include in the `config.yaml` file.
- **Deployment**: For production deployments, consider using **Lightning AI** or **Heroku**.

---

## License

This project is licensed under the MIT License.
