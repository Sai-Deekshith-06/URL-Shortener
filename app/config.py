# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     ALGORITHM: str
#     SECRET_KEY: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
#     DOMAIN_URL: str = 'http://localhost:8000/'
#     model_config = SettingsConfigDict(env_file='.env', case_sensitive=True, extra='ignore')

# settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Database Settings ---
    DATABASE_URL: str

    # --- Security Settings ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    
    # --- Application Settings ---
    DOMAIN_URL: str = "http://localhost:8000/"

    # Pydantic V2 model_config.
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True, extra='ignore')

# Create a single settings instance to be used across the application
settings = Settings()