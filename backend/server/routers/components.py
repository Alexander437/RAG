from fastapi import APIRouter

from backend.modules.dataloaders.loader import list_dataloaders
from backend.modules.embedders.embedder import list_embedders
from backend.modules.parsers.parser import list_parsers
from backend.modules.query_controllers.query_controller import list_query_controllers

router = APIRouter(prefix="/v1/components", tags=["components"])


@router.get("/parsers")
def get_parsers():
    """Возвращает все доступные парсеры"""
    parsers = list_parsers()
    return parsers


@router.get("/embedders")
def get_embedders():
    """Возвращает доступные embedders"""
    embedders = list_embedders()
    return embedders


@router.get("/dataloaders")
def get_dataloaders():
    """Возвращает доступные загрузчики данных"""
    data_loaders = list_dataloaders()
    return data_loaders


@router.get("/query_controllers")
def get_query_controllers():
    """Возвращает доступные контроллеры запросов"""
    query_controllers = list_query_controllers()
    return query_controllers
