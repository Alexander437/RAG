from typing import Dict, List

from fastapi import APIRouter

from backend.rag.dataloaders.loader import list_dataloaders
from backend.rag.embedders.embedder import list_embedders
from backend.rag.parsers.parser import list_parsers
from backend.rag.query_controllers.query_controller import list_query_controllers
from backend.rag.schemas import ComponentDto

router = APIRouter(
    prefix="/components",
    tags=["components"],
)


@router.get("/parsers")
def get_parsers() -> List[ComponentDto]:
    """Возвращает все доступные парсеры"""
    parsers = list_parsers()
    return parsers


@router.get("/embedders")
def get_embedders() -> List[ComponentDto]:
    """Возвращает доступные embedders"""
    embedders = list_embedders()
    return embedders


@router.get("/dataloaders")
def get_dataloaders() -> List[ComponentDto]:
    """Возвращает доступные загрузчики данных"""
    data_loaders = list_dataloaders()
    return data_loaders


@router.get("/query_controllers")
def get_query_controllers() -> List[ComponentDto]:
    """Возвращает доступные контроллеры запросов"""
    query_controllers = list_query_controllers()
    return query_controllers
