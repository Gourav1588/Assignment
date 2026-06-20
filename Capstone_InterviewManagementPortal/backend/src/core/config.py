from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    MONGO_URI: str
    DATABASE_NAME: str

    # Tell Pydantic to read from the .env file located in the backend root directory
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

# Instantiate the settings object for global app import
settings = Settings()