import os

import aiofiles
import requests
from typing import Optional, List, Dict
from fastapi import APIRouter, Query, File, UploadFile, HTTPException

from backend.logger import logger
from backend.rag.schemas import ModelType, EmbedderConfig, LLMConfig
from backend.settings import settings

router = APIRouter(
    prefix="/internal",
    tags=["internal"],
)


@router.post("/upload_file")
async def upload_file(
        in_file: UploadFile = File(),
        file_dir: str = "/media/alex/Elements/My_projects/RAG/data"
) -> Dict[str, str]:
    try:
        out_file_path = os.path.join(file_dir, in_file.filename)
        async with aiofiles.open(out_file_path, mode='wb') as f:
            content = await in_file.read()
            await f.write(content)
        return {"Result": "Ok"}
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))


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
                    config={"model_name": "/media/alex/Elements/My_projects/egeon/nn/lc-elastic/models/embeddings/distiluse-base-multilingual-cased-v1"}
                ).dict()
            )
        if settings.GIGACHAT_API_KEY:
            try:
                # нужно попробовать авторизоваться в gigachat
                enabled_models.append(
                    EmbedderConfig(
                        provider="gigachat",
                        config={}
                    ).dict()
                )
            except Exception as e:
                logger.error(f"Error fetching gigachat models: {e}")

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
