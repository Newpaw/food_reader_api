import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID")
    API_USERNAME: str = os.getenv('API_USERNAME')
    API_PASSWORD: str = os.getenv("API_PASSWORD")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")



settings = Settings()
