from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load .env early
load_dotenv()


class Settings(BaseSettings):
    # App
    environment: str = Field(..., env="ENVIRONMENT")

    # DB Settings
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    foundational_model: str

    # AWS Settings
    aws_region: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
