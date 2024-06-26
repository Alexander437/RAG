from typing import Optional, Sequence

from langchain.callbacks.manager import Callbacks
from langchain.docstore.document import Document
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from sentence_transformers import CrossEncoder


# More about why re-ranking is essential: https://www.mixedbread.ai/blog/mxbai-rerank-v1
class MxBaiReranker(BaseDocumentCompressor):
    """
    Сжатие документов с использованием Transformers pipeline.
    """
    model: str
    top_k: int = 3

    def compress_documents(self,
                           documents: Sequence[Document],
                           query: str,
                           callbacks: Optional[Callbacks] = None,
                           ) -> Sequence[Document]:
        """Сжатие полученного документа с учетом контекста запроса."""
        model = CrossEncoder(self.model)
        docs = [doc.page_content for doc in documents]
        reranked_docs = model.rank(query, docs, return_documents=True, top_k=self.top_k)

        documents = [
            Document(
                page_content=doc["text"], metadata=documents[doc["corpus_id"]].metadata
            )
            for doc in reranked_docs
        ]
        return documents
