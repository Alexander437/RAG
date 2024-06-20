import os

import orjson
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.auth.schemas import UserDBConfig, SMTPConfig
from backend.rag.schemas import VectorDBConfig, MetadataStoreConfig


class Settings(BaseSettings):
    """
    Класс Settings для хранения всех переменных среды
    """
    # General
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    # Auth
    USER_DB_CONFIG: UserDBConfig
    AUTH_SECRET: str = os.getenv("AUTH_SECRET", "")
    # Redis for celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    # SMTP
    SMTP_CONFIG = SMTPConfig(
        host=os.getenv("SMTP_HOST", "smtp.mail.ru"),
        port=int(os.getenv("SMTP_PORT", 587)),
        user=os.getenv("SMTP_USERNAME", ""),
        password=os.getenv("SMTP_PASSWORD", ""),
    )
    # Vector DB
    VECTOR_DB_CONFIG: VectorDBConfig
    # Metastore
    METADATA_STORE_CONFIG: MetadataStoreConfig

    # LLM
    LOCAL: bool = os.getenv("LOCAL", True)  # Allow local models
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    GIGACHAT_API_KEY: str = os.getenv("GIGACHAT_API_KEY", "")

    USER_DB_CONFIG = UserDBConfig(
        db_name=os.getenv("DB_NAME", ""),
        db_user=os.getenv("DB_USER", ""),
        db_pass=os.getenv("DB_PASS", ""),
        db_host=os.getenv("DB_HOST", ""),
        db_port=os.getenv("DB_PORT", ""),
    )
    VECTOR_DB_CONFIG = VectorDBConfig(
        provider=os.getenv("VECTORDB_PROVIDER", "qdrant"),
        config=orjson.loads(os.getenv("VECTORDB_CONFIG")),
    )
    METADATA_STORE_CONFIG = MetadataStoreConfig(
        provider=os.getenv("METADATA_PROVIDER", "file"),
        config=orjson.loads(os.getenv("METADATA_CONFIG"))
    )
    if not USER_DB_CONFIG:
        raise ValueError("USER_DB_CONFIG is not set")

    if not VECTOR_DB_CONFIG:
        raise ValueError("VECTOR_DB_CONFIG is not set")

    if not METADATA_STORE_CONFIG:
        raise ValueError("METADATA_CONFIG is not set")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
