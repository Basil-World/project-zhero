# check_models.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# This setup is the same as in our main.py
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("API Key configured successfully.")
    print("-" * 20)
    print("Attempting to list available models...\n")

    try:
        # This loop will go through all available models
        for m in genai.list_models():
            # We check if the model supports the 'generateContent' method we need
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}")
                print("-" * 20)

    except Exception as e:
        print("An error occurred while trying to list the models:")
        print(e)