# jobsearch-ai/config.py
import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env file

AI_BACKEND = os.getenv("AI_BACKEND", "openai").lower() # Default to 'openai'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Load the API key here


if AI_BACKEND == "openai" and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set, but OpenAI backend selected.")