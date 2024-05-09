# A global registry to store all available embedders.
from langchain.embeddings.base import Embeddings

from backend.settings import settings
from backend.types import EmbedderConfig

EMBEDDER_REGISTRY = {}


def register_embedder(provider: str, cls) -> None:
    """
    Регистрирует все доступные Embedders, наследованные от `BaseEmbedder`
    Args:
        provider: Ключ в EMBEDDER_REGISTRY
        cls: Класс Embedder'а
    Returns:
        None
    """
    global EMBEDDER_REGISTRY
    # Validate and add the embedder to the registry.
    if provider in EMBEDDER_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__}, already taken by {EMBEDDER_REGISTRY[provider].__name__}"
        )
    EMBEDDER_REGISTRY[provider] = cls


def get_embedder(embedder_config: EmbedderConfig) -> Embeddings:
    """
    Возвращает экземпляр Embeddings на основании конфигурации
    Args:
        embedder_config (EmbedderConfig): Конфигурация
    Returns:
        Embeddings: Объект класса Embeddings
    """
    global EMBEDDER_REGISTRY
    if embedder_config.provider not in EMBEDDER_REGISTRY:
        raise ValueError(
            f"No embedder registered with provider {embedder_config.provider}"
        )
    embedder: Embeddings = EMBEDDER_REGISTRY[embedder_config.provider](
        **embedder_config.config
    )
    return embedder


def list_embedders():
    """
    Возвращает список всех зарегистрированных Embeddings
    Returns:
        List[dict]: Список всех зарегистрированных Embeddings
    """
    global EMBEDDER_REGISTRY
    return [
        {"provider": provider, "class": cls.__name__}
        for provider, cls in EMBEDDER_REGISTRY.items()
    ]
