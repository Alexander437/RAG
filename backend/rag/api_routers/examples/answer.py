from backend.rag.query_controllers.example.payload import QUERY_WITH_VECTOR_STORE_RETRIEVER_SIMILARITY_SCORE_PAYLOAD, \
    QUERY_WITH_VECTOR_STORE_RETRIEVER_PAYLOAD, QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_PAYLOAD, \
    QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_SIMILARITY_WITH_SCORE_PAYLOAD, \
    QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_PAYLOAD, \
    QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE_PAYLOAD, \
    QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_PAYLOAD, QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE_PAYLOAD
from backend.settings import settings

example_answer_payload = {
    "vector-store-similarity": QUERY_WITH_VECTOR_STORE_RETRIEVER_PAYLOAD,
    "vector-store-similarity-threshold": QUERY_WITH_VECTOR_STORE_RETRIEVER_SIMILARITY_SCORE_PAYLOAD,

    # Search + re-ranking
    "contextual-compression-similarity": QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_PAYLOAD,
    "contextual-compression-similarity-threshold": QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_SIMILARITY_WITH_SCORE_PAYLOAD,
    # Multi-query + search + re-ranking
    "contextual-compression-multi-query-similarity": QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_PAYLOAD,
    "contextual-compression-multi-query-similarity-threshold": QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE_PAYLOAD,
    # Keeping these for future use:
    # "contextual-compression-similarity-threshold": QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_SIMILARITY_WITH_SCORE_PAYLOAD,
    # "vector-store-mmr": QUERY_WITH_VECTOR_STORE_RETRIEVER_MMR_PAYLOAD,
    # "contextual-compression-similarity": QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_PAYLOAD,
    # "multi-query-mmr": QUERY_WITH_MULTI_QUERY_RETRIEVER_MMR_PAYLOAD,
}


if settings.LOCAL:
    example_answer_payload.update(
        {
            "multi-query-similarity": QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_PAYLOAD,
            "multi-query-similarity-threshold": QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE_PAYLOAD,
        }
    )
