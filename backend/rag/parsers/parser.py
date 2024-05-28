from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, List

from langchain.docstore.document import Document

from backend.logger import logger
from backend.rag.schemas import ComponentDto

PARSER_REGISTRY = {}
PARSER_REGISTRY_EXTENSIONS = defaultdict(list)


def register_parser(name: str, cls) -> None:
    """
    Содержит все доступные парсеры
    """
    global PARSER_REGISTRY
    if name in PARSER_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__} already taken by {PARSER_REGISTRY[name].__name__}"
        )
    PARSER_REGISTRY[name] = cls
    for extension in cls.supported_file_extensions:
        PARSER_REGISTRY_EXTENSIONS[extension].append(name)


class BaseParser(ABC):
    """
    Абстрактный класс парсера.
    Содержит общие аттрибуты и методы, которые должен реализовать каждый парсер.
    """

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_chunks(self,
                         filepath: str,
                         metadata: Optional[dict],
                         *args,
                         **kwargs) -> List[Document]:
        """
        Асинхронно читает файл и возвращает его контент в chunk'ах
        Parameters:
            filepath: Путь к файлу
            metadata: Метаданные для каждого возвращаемого Document'а
        Returns:
            List[Document]: Список объектов Document, каждый является chunk'ом из исходного файла.
        """
        pass


def get_parser_for_extension(file_extension, parsers_map, *args, **kwargs) -> BaseParser | None:
    """
    При индексировании для данного file_extension возвращает нужный парсер.
    Если отображение не было найдено в parsers_map, то используется регистр по умолчанию.
    """
    global PARSER_REGISTRY_EXTENSIONS
    global PARSER_REGISTRY

    # We dont have a parser for this extension yet
    if file_extension not in PARSER_REGISTRY_EXTENSIONS:
        logger.error(f"Loaded doc with extension {file_extension} is not supported")
        return None
    # Extension not given in parser map use the default registry
    if file_extension not in parsers_map:
        # get the first parser name registered with the extension
        name = PARSER_REGISTRY_EXTENSIONS[file_extension][0]
        print(
            f"Parser map not found in the collection for extension {file_extension}. Hence, using parser {name}"
        )
        logger.debug(
            f"Parser map not found in the collection for extension {file_extension}. Hence, using parser {name}"
        )
    else:
        name = parsers_map[file_extension]
        print(
            f"Parser map found in the collection for extension {file_extension}. Hence, using parser {name}"
        )
        logger.debug(
            f"Parser map found in the collection for extension {file_extension}. Hence, using parser {name}"
        )

    if name not in PARSER_REGISTRY:
        raise ValueError(f"No parser registered with name {name}")

    return PARSER_REGISTRY[name](*args, **kwargs)


def list_parsers() -> List[ComponentDto]:
    """
    Возвращает список всех зарегистрированных парсеров
    Returns:
        List[ComponentDto]: Список с зарегистрированными парсерами
    """
    global PARSER_REGISTRY
    return [
        ComponentDto(type=parser_type, class_=cls.__name__, description=cls.__doc__.strip())
        for parser_type, cls in PARSER_REGISTRY.items()
    ]
