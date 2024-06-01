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
        db_name=os.getenv("POSTGRES_DB", ""),
        db_user=os.getenv("POSTGRES_USER", ""),
        db_pass=os.getenv("POSTGRES_PASSWORD", ""),
        db_host=os.getenv("POSTGRES_HOST", ""),
        db_port=os.getenv("POSTGRES_PORT", ""),
    )

    VECTOR_DB_CONFIG = os.getenv("VECTOR_DB_CONFIG", "")
    if not VECTOR_DB_CONFIG:
        raise ValueError("VECTOR_DB_CONFIG is not set")
    try:
        VECTOR_DB_CONFIG = VectorDBConfig.parse_obj(orjson.loads(VECTOR_DB_CONFIG))
    except Exception as e:
        raise ValueError(f"VECTOR_DB_CONFIG is invalid: {e}")

    METADATA_STORE_CONFIG = os.getenv("METADATA_STORE_CONFIG", "")
    if not METADATA_STORE_CONFIG:
        raise ValueError("METADATA_STORE_CONFIG is not set")
    try:
        METADATA_STORE_CONFIG = MetadataStoreConfig.parse_obj(
            orjson.loads(METADATA_STORE_CONFIG)
        )
    except Exception as e:
        raise ValueError(f"METADATA_STORE_CONFIG is invalid: {e}")


settings = Settings()
