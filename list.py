import requests

# API URL for listing models
api_url = "https://generativelanguage.googleapis.com/v1beta/models:listModels"
headers = {
    "X-goog-api-key": "YOUR_GEMINI_API_KEY"
}

# Make the GET request to list models
response = requests.get(api_url, headers=headers)

# Print the response for debugging
print("API Response:", response.json())
