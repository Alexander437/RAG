from typing import List

from backend.rag.schemas import ComponentDto

QUERY_CONTROLLER_REGISTRY = {}


def register_query_controller(name: str, cls) -> None:
    """
    Регистрирует все доступные контроллеры запросов
    """
    global QUERY_CONTROLLER_REGISTRY
    if name in QUERY_CONTROLLER_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__} already taken by {QUERY_CONTROLLER_REGISTRY[name].__name__}"
        )
    QUERY_CONTROLLER_REGISTRY[name] = cls


def list_query_controllers() -> List[ComponentDto]:
    """
    Возвращает список со всеми доступными контроллерами запросов
    Returns:
        List[ComponentDto]: Список доступных контроллеров запросов
    """
    global QUERY_CONTROLLER_REGISTRY
    return [
        ComponentDto(type=controller_type, class_=cls.__name__, description=cls.__doc__.strip())
        for controller_type, cls in QUERY_CONTROLLER_REGISTRY.items()
    ]
