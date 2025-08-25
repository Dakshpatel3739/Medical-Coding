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
