import requests
from typing import Optional, List
from fastapi import APIRouter, Query

from backend.logger import logger
from backend.rag.schemas import ModelType, EmbedderConfig, LLMConfig
from backend.settings import settings

router = APIRouter(
    prefix="/internal",
    tags=["internal"],
)


# @router.post("/upload-to-data-directory")

@router.get("/models")
def get_enabled_models(
    model_type: Optional[ModelType] = Query(default=None),
) -> List[dict]:
    enabled_models = []

    # Local Embedding models
    if model_type == ModelType.embedding:
        if settings.LOCAL:
            enabled_models.append(
                EmbedderConfig(
                    provider="local",
                    config={"model_name": "path_to_model"}
                ).dict()
            )

    # Local LLM models
    if model_type == ModelType.chat:
        if settings.LOCAL:
            try:
                # OLLAMA models
                url = f"{settings.OLLAMA_URL}/api/tags"
                response = requests.get(url=url)
                data = response.json()
                for model in data["models"]:
                    enabled_models.append(
                        LLMConfig(
                            name=f"ollama/{model['model']}",
                            parameters={"temperature": 0.1},
                            provider="ollama"
                        ).dict()
                    )
            except Exception as e:
                logger.error(f"Error fetching ollama models: {e}")

        if settings.GIGACHAT_API_KEY:
            try:
                # нужно попробовать авторизоваться в gigachat
                enabled_models.append(
                    LLMConfig(
                        name="GigaChat",
                        parameters={"temperature": 0.1},
                        provider="gigachat"
                    ).dict()
                )
            except Exception as e:
                logger.error(f"Error fetching gigachat models: {e}")

    return enabled_models
