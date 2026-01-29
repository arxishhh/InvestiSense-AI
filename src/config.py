from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    GITHUB_USER : str
    PROMPT_REPO : str
    POLYGON_API_KEY : str
    GEMINI_API_KEY : str
    DIR : str



    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        extras = "ignore"
    )

Config = Settings()