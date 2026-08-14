from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("API Key Loaded:", api_key is not None)

genai.configure(api_key=api_key)

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)