import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    AI_API_URL = os.getenv("AI_API_URL")
    DATABASE_URL = "sqlite:///./buildings.db"
