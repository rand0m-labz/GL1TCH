# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    AGENT_NAME = os.getenv("AGENT_NAME", "GL1TCH")
    AGENT_PORT = int(os.getenv("AGENT_PORT", 8080))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    N8N_USER = os.getenv("N8N_BASIC_AUTH_USER", "admin")
    N8N_PASS = os.getenv("N8N_BASIC_AUTH_PASSWORD", "gl1tchadmin")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

config = Config()