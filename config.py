import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# AI Model configs
AVAILABLE_MODELS = {
    "Gemini": "gemini-1.5-flash",
    "OpenAI": "gpt-3.5-turbo"
}

DEFAULT_MODEL = "Gemini"
