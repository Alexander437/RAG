import os

import orjson
from pydantic_settings import BaseSettings

from backend.auth.schemas import UserDBConfig
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
    # Vector DB
    VECTOR_DB_CONFIG: VectorDBConfig
    # Metastore
    METADATA_STORE_CONFIG: MetadataStoreConfig

    # LLM
    LOCAL: bool = os.getenv("LOCAL", True)
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    GIGACHAT_API_KEY: str = os.getenv("GIGACHAT_API_KEY", "")

    USER_DB_CONFIG = UserDBConfig(
        db_name=os.getenv("DB_NAME", ""),
        db_user=os.getenv("DB_USER", ""),
        db_pass=os.getenv("DB_PASS", ""),
        db_host=os.getenv("DB_HOST", ""),
        db_port=os.getenv("DB_PORT", ""),
    )
    METADATA_STORE_CONFIG = MetadataStoreConfig(
        provider=os.getenv("METADATA_PROVIDER", "file"),
        config=orjson.loads(os.getenv("METADATA_CONFIG"))
    )

    VECTOR_DB_CONFIG = os.getenv("VECTOR_DB_CONFIG", "")
    if not VECTOR_DB_CONFIG:
        raise ValueError("VECTOR_DB_CONFIG is not set")
    VECTOR_DB_CONFIG = VectorDBConfig.parse_obj(orjson.loads(VECTOR_DB_CONFIG))

    if not METADATA_STORE_CONFIG:
        raise ValueError("METADATA_CONFIG is not set")


settings = Settings()
