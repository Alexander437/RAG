from typing import List

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


def list_query_controllers() -> List[dict]:
    """
    Возвращает список со всеми доступными контроллерами запросов
    Returns:
        List[dict]: Список доступных контроллеров запросов
    """
    global QUERY_CONTROLLER_REGISTRY
    return [
        {
            "type": controller_type,
            "class": cls.__name__,
        }
        for controller_type, cls in QUERY_CONTROLLER_REGISTRY.items()
    ]
