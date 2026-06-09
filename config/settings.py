from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """
    Centralized project configuration.
    """

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

    BESTTIME_API_KEY = os.getenv("BESTTIME_API_KEY")

    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")


settings = Settings()