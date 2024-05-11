from typing import Any, ClassVar, Collection, Dict, Optional

from pydantic import BaseModel, Field, root_validator, validator
from qdrant_client.models import Filter as QdrantFilter

from backend.types import LLMConfig

GENERATION_TIMEOUT_SEC = 60.0 * 5


class VectorStoreRetrieverConfig(BaseModel):
    """
    Конфигурация VectorStore Retriever
    """

    search_type: str = Field(
        default="similarity",
        title="""Определяет тип поиска, который реализует Retriever. Может быть 'similarity' (по умолчанию), 'mmr', или
          'similarity_score_threshold'.
            - "similarity": возвращает первые k ближайших к запросу,
            - "mmr": возвращает первые k ближайших к запросу и ранжирует их в соответствии с алгоритмом MMR,
            - "similarity_score_threshold": возвращает все документы, близость которых превышает порог
        """,
    )

    search_kwargs: dict = Field(default_factory=dict)

    filter: Optional[dict] = Field(
        default_factory=dict,
        title="""Фильтрация по метаданным документа""",
    )

    allowed_search_types: ClassVar[Collection[str]] = (
        "similarity",
        "similarity_score_threshold",
        "mmr",
    )

    @root_validator
    def validate_search_type(cls, values: Dict) -> Dict:
        """Проверка search type."""
        search_type = values.get("search_type")

        assert (
            search_type in cls.allowed_search_types
        ), f"search_type of {search_type} not allowed. Valid values are: {cls.allowed_search_types}"

        search_kwargs = values.get("search_kwargs")

        if search_type == "similarity":
            assert "k" in search_kwargs, "k is required for similarity search"

        elif search_type == "mmr":
            assert "k" in search_kwargs, "k is required in search_kwargs for mmr search"
            assert (
                "fetch_k" in search_kwargs
            ), "fetch_k is required in search_kwargs for mmr search"

        elif search_type == "similarity_score_threshold":
            assert (
                "score_threshold" in search_kwargs
            ), "score_threshold with a float value(0~1) is required in search_kwargs for similarity_score_threshold search"

        # filters = values.get("filter")
        # if filters:
        #     search_kwargs["filter"] = QdrantFilter.parse_obj(filters)
        return values


class MultiQueryRetrieverConfig(VectorStoreRetrieverConfig):
    retriever_llm_configuration: LLMConfig = Field(
        title="LLM конфигурация для retriever",
    )


class ContextualCompressionRetrieverConfig(VectorStoreRetrieverConfig):
    compressor_model_provider: str = Field(
        title="Поставщик compressor model",
    )

    compressor_model_name: str = Field(
        title="model name of the compressor",
    )

    top_k: int = Field(
        title="Top K docs to collect post compression",
    )

    allowed_compressor_model_providers: ClassVar[Collection[str]] = ("mixbread-ai",)

    @validator("compressor_model_provider")
    def validate_retriever_type(cls, value) -> Dict:
        assert (
            value in cls.allowed_compressor_model_providers
        ), f"Compressor model of {value} not allowed. Valid values are: {cls.allowed_compressor_model_providers}"
        return value


class ContextualCompressionMultiQueryRetrieverConfig(
    ContextualCompressionRetrieverConfig, MultiQueryRetrieverConfig
):
    pass


class LordOfRetrievers(ContextualCompressionRetrieverConfig, MultiQueryRetrieverConfig):
    pass


class ExampleQueryInput(BaseModel):
    """
    Модель для ввода запросов.
    Требует указания collection name, retriever configuration, query, LLM configuration и prompt template.
    """

    collection_name: str = Field(
        default=None,
        title="Имя коллекции, по которой проводится поиск",
    )

    query: str = Field(title="Запрос для поиска")

    model_configuration: LLMConfig

    prompt_template: str = Field(
        title="Шаблон для промпта для генерации ответа с учетом контекста",
    )

    retriever_name: str = Field(
        title="Retriever name",
    )

    retriever_config: Dict[str, Any] = Field(
        title="Конфигурация Retriever",
    )

    allowed_retriever_types: ClassVar[Collection[str]] = (
        "vectorstore",
        "multi-query",
        "contexual-compression",
        "contexual-compression-multi-query",
        "lord-of-the-retrievers",
    )

    stream: Optional[bool] = Field(title="Stream the results", default=False)

    @root_validator()
    def validate_retriever_type(cls, values: Dict) -> Dict:
        retriever_name = values.get("retriever_name")

        assert (
            retriever_name in cls.allowed_retriever_types
        ), f"retriever of {retriever_name} not allowed. Valid values are: {cls.allowed_retriever_types}"

        if retriever_name == "vectorstore":
            values["retriever_config"] = VectorStoreRetrieverConfig(
                **values.get("retriever_config")
            )

        elif retriever_name == "multi-query":
            values["retriever_config"] = MultiQueryRetrieverConfig(
                **values.get("retriever_config")
            )

        elif retriever_name == "contexual-compression":
            values["retriever_config"] = ContextualCompressionRetrieverConfig(
                **values.get("retriever_config")
            )

        elif retriever_name == "contexual-compression-multi-query":
            values["retriever_config"] = ContextualCompressionMultiQueryRetrieverConfig(
                **values.get("retriever_config")
            )

        elif retriever_name == "lord-of-the-retrievers":
            values["retriever_config"] = LordOfRetrievers(
                **values.get("retriever_config")
            )

        return values
