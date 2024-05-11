from abc import ABC, abstractmethod
from typing import Any, Dict, List

from backend.constants import DATA_POINT_FQN_METADATA_KEY, FQN_SEPARATOR
from backend.types import (
    AssociateDataSourceWithCollection,
    Collection,
    CreateCollection,
    CreateDataIngestionRun,
    CreateDataSource,
    DataIngestionRun,
    DataIngestionRunStatus,
    DataSource,
    MetadataStoreConfig,
)


class BaseMetadataStore(ABC):
    @abstractmethod
    def create_collection(self, collection: CreateCollection) -> Collection:
        """
        Создание коллекции в metadata store
        """
        raise NotImplementedError

    @abstractmethod
    def get_collection_by_name(self,
                               collection_name: str,
                               no_cache: bool = True) -> Collection | None:
        """
        Доступ к коллекции по имени
        """
        raise NotImplementedError()

    @abstractmethod
    def get_collections(self) -> List[Collection]:
        """
        Возвращает список всех коллекций metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def create_data_source(self, data_source: CreateDataSource) -> DataSource:
        """
        Создает источник данных в metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data_source_from_fqn(self, fqn: str) -> DataSource | None:
        """
        Возвращает источник данных в соответствии с его fqn metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data_sources(self) -> List[DataSource]:
        """
        Возвращает список всех источников данных в metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def create_data_ingestion_run(self,
                                  data_ingestion_run: CreateDataIngestionRun
                                  ) -> DataIngestionRun:
        """
        Возвращает экземпляр задачи по передаче данных в metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data_ingestion_run(self,
                               data_ingestion_run_name: str,
                               no_cache: bool = False
                               ) -> DataIngestionRun | None:
        """
        Возвращает экземпляр задачи по передаче данных из metadata store по имени
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data_ingestion_runs(self,
                                collection_name: str,
                                data_source_fqn: str = None
                                ) -> List[DataIngestionRun]:
        """
        Возвращает все экземпляры задач по передаче всех данных из metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_collection(self, collection_name: str, include_runs=False):
        """
        Удаляет коллекцию из metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def associate_data_source_with_collection(self,
                                              collection_name: str,
                                              data_source_association: AssociateDataSourceWithCollection
                                              ) -> Collection:
        """
        Связывает источник данных с коллекцией metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def unassociate_data_source_with_collection(self,
                                                collection_name: str,
                                                data_source_fqn: str
                                                ) -> Collection:
        """
        Удаляет связь между источником данных и коллекцией metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def update_data_ingestion_run_status(self,
                                         data_ingestion_run_name: str,
                                         status: DataIngestionRunStatus):
        """
        Обновляет статус приема данных в metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def log_metrics_for_data_ingestion_run(self,
                                           data_ingestion_run_name: str,
                                           metric_dict: dict[str, int | float],
                                           step: int = 0):
        """
        Логирует метрики задачи приема данных в metadata store
        """
        raise NotImplementedError()

    @abstractmethod
    def log_errors_for_data_ingestion_run(self,
                                          data_ingestion_run_name: str,
                                          errors: Dict[str, Any]):
        """
        Логирует ошибки задачи приема данных в the metadata store
        """
        raise NotImplementedError()


def get_data_source_fqn(data_source: CreateDataSource) -> str:
    return f"{FQN_SEPARATOR}".join([data_source.type, data_source.uri])


def get_data_source_fqn_from_document_metadata(document_metadata: Dict[str, str]) -> str | None:
    if document_metadata and document_metadata.get(DATA_POINT_FQN_METADATA_KEY):
        parts = document_metadata.get(DATA_POINT_FQN_METADATA_KEY).split(FQN_SEPARATOR)
        if len(parts) == 3:
            return f"{FQN_SEPARATOR}".join(parts[:2])


# A global registry to store all available metadata store.
METADATA_STORE_REGISTRY = {}


def register_metadata_store(provider: str, cls) -> None:
    """
    Регистрирует все доступные metadata store.
    Args:
        provider: Тип регистрируемой metadata store
        cls: Класс регистрируемой metadata store
    Returns:
        None
    """
    global METADATA_STORE_REGISTRY
    if provider in METADATA_STORE_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__} already taken by {METADATA_STORE_REGISTRY[provider].__name__}"
        )
    METADATA_STORE_REGISTRY[provider] = cls


def get_metadata_store_client(config: MetadataStoreConfig) -> BaseMetadataStore:
    if config.provider in METADATA_STORE_REGISTRY:
        return METADATA_STORE_REGISTRY[config.provider](config=config.config)
    else:
        raise ValueError(f"Unknown metadata store type: {config.provider}")
