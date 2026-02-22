from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    GITHUB_USER : str
    PROMPT_REPO : str
    GEMINI_API_KEY : str
    DIR : str
    URL_DATABASE : str
    GROQ_API_KEY : str
    GROQ_MODEL : str
    IDENTITY : str
    TAVILY_API_KEY : str
    JWT_SECRET : str
    JWT_ALGORITHM : str


    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        extras = "ignore"
    )

Config = Settings()