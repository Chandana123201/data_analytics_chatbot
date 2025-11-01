import os
from google import genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
