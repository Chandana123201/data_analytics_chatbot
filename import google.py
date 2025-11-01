import google.generativeai as genai
import os

# Load the API key securely from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("\nAvailable models in your account:\n")
for m in genai.list_models():
    print(m.name)

