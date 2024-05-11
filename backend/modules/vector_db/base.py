from abc import ABC, abstractmethod
from typing import List

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.schema.vectorstore import VectorStore

from backend.constants import DEFAULT_BATCH_SIZE_FOR_VECTOR_STORE
from backend.types import DataPointVector


class BaseVectorDB(ABC):
    @abstractmethod
    def create_collection(self, collection_name: str, embeddings: Embeddings):
        """
        Создает коллекцию в векторной БД
        """
        raise NotImplementedError()

    @abstractmethod
    def upsert_documents(self,
                         collection_name: str,
                         documents: List[Document],
                         embeddings: Embeddings,
                         incremental: bool = True):
        """
        Загружает документы в векторную БД
        """
        raise NotImplementedError()

    @abstractmethod
    def get_collections(self) -> List[str]:
        """
        Возвращает имена всех коллекций векторной БД
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_collection(self, collection_name: str):
        """
        Удаляет коллекцию из векторной БД
        """
        raise NotImplementedError()

    @abstractmethod
    def get_vector_store(self,
                         collection_name: str,
                         embeddings: Embeddings) -> VectorStore:
        """
        Возвращает vector store
        """
        raise NotImplementedError()

    @abstractmethod
    def get_vector_client(self):
        """
        Возвращает vector client
        """
        raise NotImplementedError()

    @abstractmethod
    def list_data_point_vectors(self,
                                collection_name: str,
                                data_source_fqn: str,
                                batch_size: int = DEFAULT_BATCH_SIZE_FOR_VECTOR_STORE,
                                ) -> List[DataPointVector]:
        """
        Возвращает векторы из коллекции
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_data_point_vectors(self,
                                  collection_name: str,
                                  data_point_vectors: List[DataPointVector],
                                  batch_size: int = DEFAULT_BATCH_SIZE_FOR_VECTOR_STORE):
        """
        Удаляет векторы из коллекции
        """
        raise NotImplementedError()
