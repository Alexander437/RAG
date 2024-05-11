import os
from typing import Optional

import orjson
from pydantic import BaseSettings

from backend.types import MetadataStoreConfig, VectorDBConfig


class Settings(BaseSettings):
    """
    Класс Settings для хранения всех переменных среды
    """
    LOCAL: bool
    LOG_LEVEL: str
    GIGACHAT_API_KEY: str
    VECTOR_DB_CONFIG: VectorDBConfig
    METADATA_STORE_CONFIG: MetadataStoreConfig

    LOCAL: bool = os.getenv("LOCAL", True)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
    GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY", "")
    VECTOR_DB_CONFIG = os.getenv("VECTOR_DB_CONFIG", "")
    METADATA_STORE_CONFIG = os.getenv("METADATA_STORE_CONFIG", "")

    # Для backend.indexer.indexer -> ingest_data(request)
    JOB_FQN = os.getenv("JOB_FQN", "")
    JOB_COMPONENT_NAME = os.getenv("JOB_COMPONENT_NAME", "")

    """
    VECTOR_DB_CONFIG: VectorDBConfig
    TFY_SERVICE_ROOT_PATH: Optional[str] = "/"
    TFY_API_KEY: str
    GIGACHAT_API_KEY: Optional[str]
    TFY_HOST: Optional[str]
    TFY_LLM_GATEWAY_URL: str
    EMBEDDING_CACHE_CONFIG: Optional[EmbeddingCacheConfig] = None

    VECTOR_DB_CONFIG = os.getenv("VECTOR_DB_CONFIG", "")
    METADATA_STORE_CONFIG = os.getenv("METADATA_STORE_CONFIG", "")
    TFY_SERVICE_ROOT_PATH = os.getenv("TFY_SERVICE_ROOT_PATH", "")
    JOB_FQN = os.getenv("JOB_FQN", "")
    JOB_COMPONENT_NAME = os.getenv("JOB_COMPONENT_NAME", "")
    TFY_API_KEY = os.getenv("TFY_API_KEY", "")
    GIGACHAT_API_KEY = os.getenv("OPENAI_API_KEY", "")
    TFY_HOST = os.getenv("TFY_HOST", "")
    TFY_LLM_GATEWAY_URL = os.getenv("TFY_LLM_GATEWAY_URL", "")


    LOCAL: bool = os.getenv("LOCAL", False)
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    """
    """
    if not VECTOR_DB_CONFIG:
        raise ValueError("VECTOR_DB_CONFIG is not set")

    if not METADATA_STORE_CONFIG:
        raise ValueError("METADATA_STORE_CONFIG is not set")

    if not TFY_LLM_GATEWAY_URL:
        TFY_LLM_GATEWAY_URL = f"{TFY_HOST}/api/llm"

    try:
        VECTOR_DB_CONFIG = VectorDBConfig.parse_obj(orjson.loads(VECTOR_DB_CONFIG))
    except Exception as e:
        raise ValueError(f"VECTOR_DB_CONFIG is invalid: {e}")
    try:
        METADATA_STORE_CONFIG = MetadataStoreConfig.parse_obj(
            orjson.loads(METADATA_STORE_CONFIG)
        )
    except Exception as e:
        raise ValueError(f"METADATA_STORE_CONFIG is invalid: {e}")
    """


settings = Settings()
