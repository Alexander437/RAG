from abc import ABC, abstractmethod
from typing import Dict, Iterator, List

from backend.types import DataIngestionMode, DataPoint, DataSource, LoadedDataPoint

# A global registry to store all available loaders.
LOADER_REGISTRY = {}


def register_dataloader(loader_type: str, cls) -> None:
    """
    Все доступные загрузчики регистрируются с использованием класса `BaseDataLoader`

    Args:
        loader_type: тип загрузчика, который регистрируется
        cls: класс загрузчика, который регистрируется

    Returns:
        None
    """
    global LOADER_REGISTRY
    # Validate and add the loader to the registry
    if not loader_type:
        raise ValueError(
            f"static attribute 'name' needs to be a non-empty string on class {cls.__name__}"
        )
    if loader_type in LOADER_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__}, 'name' already taken by {LOADER_REGISTRY[type].__name__}"
        )
    LOADER_REGISTRY[loader_type] = cls


class BaseDataLoader(ABC):
    """
    Базовый класс загрузчика данных. Отвечает за обнаружение, фильтрацию и загрузку точек данных.
    """

    def load_full_data(self,
                       data_source: DataSource,
                       dest_dir: str,
                       batch_size: int = 100) -> Iterator[List[LoadedDataPoint]]:
        """
        Синхронизирует источник данных и загружает все точки данных из источника в каталог
        Args:
            data_source (DataSource): Источник данных
            dest_dir (str): Директория, в которую записываются принимаемые данные
            batch_size (int): Размер батча при загрузке точек данных
        Returns:
            Iterator[List[LoadedDataPoint]]: Итератор со списками точек данных
        """
        return self.load_filtered_data(
            data_source,
            dest_dir,
            previous_snapshot={},
            batch_size=batch_size,
            data_ingestion_mode=DataIngestionMode.FULL,
        )

    def load_incremental_data(self,
                              data_source: DataSource,
                              dest_dir: str,
                              previous_snapshot: Dict[str, str],
                              batch_size: int = 100) -> Iterator[List[LoadedDataPoint]]:
        """
        Синхронизирует источник данных, фильтрует точки данных и загружает их из источника в каталог
        Args:
            data_source (DataSource): Источник, из которого загружаются данные
            dest_dir (str): Директория, в которую загружаются данные
            previous_snapshot (Dict[str, str]): Словарь с существующими точками данных
            batch_size (int): Размер батча, используемый при загрузке данных
        Returns:
            Iterator[List[LoadedDataPoint]]: Итератор со списками точек данных
        """
        return self.load_filtered_data(
            data_source,
            dest_dir,
            previous_snapshot,
            batch_size=batch_size,
            data_ingestion_mode=DataIngestionMode.INCREMENTAL,
        )

    @abstractmethod
    def load_filtered_data(self,
                           data_source: DataSource,
                           dest_dir: str,
                           previous_snapshot: Dict[str, str],
                           batch_size: int,
                           data_ingestion_mode: DataIngestionMode) -> Iterator[List[LoadedDataPoint]]:
        """
        Синхронизирует источник данных, фильтрует точки данных и загружает их из источника в директорию.
        Метод возвращает загруженные точки данных в батчах в виде итератора.
        Args:
            data_source (DataSource): Источник, из которого загружаются данные
            dest_dir (str): Директория, в которую загружаются данные
            previous_snapshot (Dict[str, str]): Словарь с существующими точками данных
            batch_size (int): Размер батча, используемый при загрузке данных
            data_ingestion_mode (DataIngestionMode): Режим приема данных
        Returns:
            Iterator[List[LoadedDataPoint]]: Итератор со списками точек данных
        """
        pass


def get_loader_for_data_source(loader_type, *args, **kwards) -> BaseDataLoader:
    """
    Возвращает объект загрузчика заданного типа
    Args:
        loader_type (str): Тип загрузчика
    Returns:
        BaseLoader: Объект загрузчика
    """
    global LOADER_REGISTRY
    if loader_type not in LOADER_REGISTRY:
        raise ValueError(f"No loader registered with type {loader_type}")
    return LOADER_REGISTRY[loader_type](*args, **kwards)


def list_dataloaders() -> List[dict]:
    """
    Возвращает список всех зарегистрированных загрузчиков
    Returns:
        List[dict]: Список всех зарегистрированных загрузчиков
    """
    global LOADER_REGISTRY
    return [
        {"type": loader_type, "class": cls.__name__, "description": cls.__doc__strip()}
        for loader_type, cls in LOADER_REGISTRY.items()
    ]
