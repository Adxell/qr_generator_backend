from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings): 
    gemini_key: str

    model_config = SettingsConfigDict(env_file=".env.dev")

settings = Settings()