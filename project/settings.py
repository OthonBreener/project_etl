from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
        env_file_enconding='utf-8',
    )

    POSTGRES_FONTE_USER: str
    POSTGRES_FONTE_PASSWORD: str
    POSTGRES_FONTE_DB: str
    POSTGRES_ALVO_USER: str
    POSTGRES_ALVO_PASSWORD: str
    POSTGRES_ALVO_DB: str
