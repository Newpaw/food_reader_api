import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID")
    API_USERNAME: str = os.getenv('API_USERNAME')
    API_PASSWORD: str = os.getenv("API_PASSWORD")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_HOST:str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT:str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB:str = os.getenv("POSTGRES_DB")
    DATABASE_URL:str = os.getenv("DATABASE_URL")





settings = Settings()
