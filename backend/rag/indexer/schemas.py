from pydantic import BaseModel, Field
from backend.rag.schemas import DataIngestionMode, DataSource, EmbedderConfig, ParserConfig


class DataIngestionConfig(BaseModel):
    """
    Класс для хранения конфигурации приема данных
    """
    collection_name: str = Field(
        title="a unique name to your collection",
    )
    data_ingestion_run_name: str = Field(
        title="a unique name to your ingestion run",
    )
    data_source: DataSource = Field(
        title="Data source to ingest data from. Can be local or github",
    )
    embedder_config: EmbedderConfig = Field(
        title="Embedder configuration",
    )
    parser_config: ParserConfig = Field(
        title="Parser configuration to parse the documents.",
    )
    data_ingestion_mode: DataIngestionMode = Field(
        title="Data ingestion mode",
    )
    raise_error_on_failure: bool = Field(
        title="Raise error on failure",
        default=True,
    )
    batch_size: int = Field(
        title="Batch size for indexing",
        ge=1, default=100,
    )
