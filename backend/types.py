from enum import Enum
from typing import List, Optional, Dict, Any, Literal

from pydantic import BaseModel, Field, root_validator  # model_validator

from backend.constants import FQN_SEPARATOR


class DataIngestionMode(str, Enum):
    """
    Режимы приема данных
    """
    NONE = "NONE"
    INCREMENTAL = "INCREMENTAL"
    FULL = "FULL"


class DataPoint(BaseModel):
    """
    Описывает одну точку данных в источнике данных
    аттрибуты:
    - data_source_fqn (str): Полное имя источника данных
    - data_point_fqn (str): Полное имя точки данных относительно источника
    - data_point_uri (str): URI точки данных для данного источника (url, путь к файлу и др.)
    - data_point_hash (str): Хэш точки данных в данном источнике, который будет обновляться при обновлении точки данных
    - metadata (Optional[Dict[str, str]]): Метаданные для точки данных
    """
    data_source_fqn: str = Field(
        title="Fully qualified name of the data resource",
    )

    data_point_uri: str = Field(
        title="URI for the data point for given data source (url, file path, etc)",
    )

    data_point_hash: str = Field(
        title="Hash of the data point for the given data source",
    )

    metadata: Optional[Dict[str, str]] = Field(
        title="Additional metadata for the data point",
    )

    @property
    def data_point_fqn(self) -> str:
        return f"{FQN_SEPARATOR}".join([self.data_source_fqn, self.data_point_uri])


class DataPointVector(BaseModel):
    """
    Вектор точки данных, описывающий ее в векторной БД
    Дополнительные аттрибуты:
    - data_point_vector_id (str): Уникальный идентификатор точки в векторной БД
    - data_point_fqn (str): Уникальный идентификатор точки данных в источнике данных
    - data_point_hash (str): Хэш точки данных, для данного источника данных, который будет обновляться при обновлении точки данных
    """
    data_point_vector_id: str = Field(
        title="Unique identifier for the data point with respect to the vector store",
    )
    data_point_fqn: str = Field(
        title="Unique identifier for the data point with respect to the data source",
    )
    data_point_hash: str = Field(
        title="Hash of the data point for the given data source",
    )


class LoadedDataPoint(DataPoint):
    """
    Загруженная точка данных, описывает точку данных после ее загрузки как локального файла
    Дополнительные аттрибуты:
    - local_filepath (str): путь к файлу с точкой данных
    - file_extension (str): расширение файла с точкой данных
    """
    local_filepath: str = Field(
        title="Local file path of the loaded data point",
    )
    file_extension: Optional[str] = Field(
        title="File extension of the loaded data point",
    )


class EmbedderConfig(BaseModel):
    """
    Конфигурация Embedder
    """
    provider: str = Field(
        title="Provider of the embedder",
    )
    config: Optional[Dict[str, Any]] = Field(
        title="Configuration for the embedder", default={"model": "string"}
    )


class ParserConfig(BaseModel):
    """
    Parser configuration
    """
    chunk_size: int = Field(
        title="Chunk size for data parsing", ge=1, default=1000
    )
    chunk_overlap: int = Field(
        title="Chunk Overlap for indexing", ge=0, default=20
    )
    parse_map: Dict[str, str] = Field(
        title="Mapping of the file extensions to parsers",
        default={
            ".md": "MarkdownParser",
            ".pdf": "PdfParserFast",
        },
    )
    additional_config: Optional[Dict[str, Any]] = Field(
        title="Additional optional configuration for the parser",
        default={"key": "value"},
    )


class VectorDBConfig(BaseModel):
    """
    Конфигурация векторной ДБ
    """
    provider: str
    local: Optional[bool] = None
    url: Optional[str] = None
    api_key: Optional[str] = None
    config: Optional[dict] = None


class MetadataStoreConfig(BaseModel):
    """
    Конфигурация хранилища метаданных
    """
    provider: str
    config: Optional[dict] = None


class EmbeddingCacheConfig(BaseModel):
    """
    Embedding cache configuration
    """
    provider: str
    url: Optional[str] = None
    config: Optional[dict] = None


class LLMConfig(BaseModel):
    """
    Конфигурация LLM
    """
    name: str = Field(title="Name of the model")
    parameters: dict = None
    provider: Literal["openai", "ollama", "truefoundry"] = Field(
        title="Model provider any one between openai, ollama, truefoundry",
        default="truefoundry",
    )


class RetrieverConfiguration(BaseModel):
    """
    Конфигурация поиска в векторной БД
    * mmr - баланс между релевантностью и разнообразием
    """
    search_type: Literal["mmr", "similarity"] = Field(
        default="similarity",
        title="""Defines the type of search that the Retriever should perform. Can be "similarity" (default), "mmr", 
         or "similarity_score_threshold".""",
    )
    k: int = Field(
        default=4,
        title="Amount of documents to return (Default: 4)",
    )
    fetch_k: int = Field(
        default=20,
        title="Amount of documents to pass to MMR algorithm (Default: 20)",
    )
    filter: Optional[dict] = Field(
        default=None,
        title="Filter by document metadata",
    )

    @property
    def get_search_type(self) -> str:
        # Check at langchain.schema.vectorstore.VectorStore.as_retriever
        return self.search_type

    @property
    def get_search_kwargs(self) -> dict:
        # Check at langchain.schema.vectorstore.VectorStore.as_retriever
        match self.search_type:
            case "similarity":
                return {"k": self.k, "filter": self.filter}
            case "mmr":
                return {"k": self.k, "fetch_k": self.fetch_k, "filter": self.filter}


class DataIngestionRunStatus(str, Enum):
    """
    Определяет статус выполнения задачи приема данных в векторную БД
    """
    INITIALIZED = "INITIALIZED"
    FETCHING_EXISTING_VECTORS = "FETCHING_EXISTING_VECTORS"
    FETCHING_EXISTING_VECTORS_FAILED = "FETCHING_EXISTING_VECTORS_FAILED"
    DATA_INGESTION_STARTED = "DATA_INGESTION_STARTED"
    DATA_INGESTION_COMPLETED = "DATA_INGESTION_COMPLETED"
    DATA_INGESTION_FAILED = "DATA_INGESTION_FAILED"
    DATA_CLEANUP_STARTED = "DATA_CLEANUP_STARTED"
    DATA_CLEANUP_FAILED = "DATA_CLEANUP_FAILED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class BaseDataIngestionRun(BaseModel):
    """
    Базовая конфигурация задач приема данных
    """
    collection_name: str = Field(
        title="Name of the collection",
    )
    data_source_fqn: str = Field(
        title="Fully qualified name of the data source",
    )
    parser_config: ParserConfig = Field(
        title="Parser configuration for the data transformation", default_factory=dict
    )
    data_ingestion_mode: DataIngestionMode = Field(
        default=DataIngestionMode.INCREMENTAL,
        title="Data ingestion mode for the data ingestion",
    )
    raise_error_on_failure: Optional[bool] = Field(
        title="Flag to configure weather to raise error on failure or not. Default is True",
        default=True,
    )


class CreateDataIngestionRun(BaseDataIngestionRun):
    pass


class DataIngestionRun(BaseDataIngestionRun):
    name: str = Field(
        title="Name of the data ingestion run",
    )
    status: Optional[DataIngestionRunStatus] = Field(
        title="Status of the data ingestion run",
    )


class BaseDataSource(BaseModel):
    """
    Конфигурация источника данных
    """
    type: str = Field(
        title="Type of the data source",
    )
    uri: str = Field(
        title="A unique identifier for the data source",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        title="Additional config for your data source"
    )

    @property
    def fqn(self):
        return f"{FQN_SEPARATOR}".join([self.type, self.uri])

    @root_validator  # @model_validator(mode="after")
    def validate_fqn(self, values: Dict) -> Dict:
        values["fqn"] = f"{FQN_SEPARATOR}".join([values["type"], values["uri"]])
        return values


class CreateDataSource(BaseDataSource):
    pass


class DataSource(BaseDataSource):
    pass


class AssociatedDataSources(BaseModel):
    """
    Конфигурация связанного источника данных
    """
    data_source_fqn: str = Field(
        title="Fully qualified name of the data source",
    )
    parser_config: ParserConfig = Field(
        title="Parser configuration for the data transformation", default_factory=dict
    )
    data_source: Optional[DataSource] = Field(
        title="Data source associated with the collection"
    )


class IngestDataToCollectionDto(BaseModel):
    """
    Конфигурация для приема данных в коллекцию
    """
    collection_name: str = Field(
        title="Name of the collection",
    )
    data_source_fqn: Optional[str] = Field(
        title="Fully qualified name of the data source",
    )
    data_ingestion_mode: DataIngestionMode = Field(
        default=DataIngestionMode.INCREMENTAL,
        title="Data ingestion mode for the data ingestion",
    )
    raise_error_on_failure: Optional[bool] = Field(
        title="Flag to configure weather to raise error on failure or not. Default is True",
        default=True,
    )
    run_as_job: bool = Field(
        title="Flag to configure weather to run the ingestion as a job or not. Default is False",
        default=False,
    )
    batch_size: int = Field(
        title="Batch size for data ingestion",
        default=100,
    )


class AssociateDataSourceWithCollection(BaseModel):
    """
    Конфигурация связи источника данных с коллекцией
    """
    data_source_fqn: str = Field(
        title="Fully qualified name of the data source",
    )
    parser_config: ParserConfig = Field(
        title="Parser configuration for the data transformation", default_factory=dict
    )


class AssociateDataSourceWithCollectionDto(AssociateDataSourceWithCollection):
    """
    Конфигурация связи источника данных с коллекцией
    DTO --> Data Transfer Object
    """
    collection_name: str = Field(
        title="Name of the collection",
    )
    data_source_fqn: str = Field(
        title="Fully qualified name of the data source",
    )
    parser_config: ParserConfig = Field(
        title="Parser configuration for the data transformation", default_factory=dict
    )


class UnassociateDataSourceWithCollectionDto(BaseModel):
    """
    Конфигурация для открепления источника данных от коллекции
    """
    collection_name: str = Field(
        title="Name of the collection",
    )
    data_source_fqn: str = Field(
        title="Fully qualified name of the data source",
    )


class BaseCollection(BaseModel):
    """
    Базовая конфигурация коллекции
    """
    name: constr(regex=r"^[a-z][a-z0-9]*$") = Field(  # type: ignore
        title="a unique name to your collection",
        description="Should only contain lowercase alphanumeric character",
    )
    description: Optional[str] = Field(
        title="a description for your collection",
    )
    embedder_config: EmbedderConfig = Field(
        title="Embedder configuration", default_factory=dict
    )


class CreateCollection(BaseCollection):
    pass


class Collection(BaseCollection):
    associated_data_sources: Dict[str, AssociatedDataSources] = Field(
        title="Data sources associated with the collection", default_factory=dict
    )


class CreateCollectionDto(CreateCollection):
    associated_data_sources: Optional[List[AssociateDataSourceWithCollection]] = Field(
        title="Data sources associated with the collection"
    )


class UploadToDataDirectoryDto(BaseModel):
    filepaths: List[str]


class ModelType(str, Enum):
    """
    Типы моделей, доступные в шлюзе LLM
    """
    completion = "completion"
    chat = "chat"
    embedding = "embedding"


class ListDataIngestionRunsDto(BaseModel):
    collection_name: str = Field(
        title="Name of the collection",
    )
    data_source_fqn: Optional[str] = Field(
        title="Fully qualified name of the data source", default=None
    )
