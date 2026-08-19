# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ollama config
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "qwen2.5:0.5b"
    embed_model_name: str = "mxbai-embed-large:latest"

    # Database config
    database_url: str = ""

    # App config
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
