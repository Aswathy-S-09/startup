from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models = [
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-pro",
    "gemini-pro-latest",
]

for model in models:
    print(f"\nTesting {model}")

    try:
        response = client.models.generate_content(
            model=model,
            contents="Say Hello"
        )
        print("✅ Works")
        print(response.text)
    except Exception as e:
        print("❌", e)