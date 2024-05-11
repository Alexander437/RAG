QUERY_WITH_VECTOR_STORE_RETRIEVER_SIMILARITY = {
    "collection_name": "example",
    "query": "Что говорится в Конституции по поводу защиты информации?",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "vectorstore",
    "retriever_config": {"search_type": "similarity", "search_kwargs": {"k": 5}},
    "stream": False,
}

QUERY_WITH_VECTOR_STORE_RETRIEVER_PAYLOAD = {
    "summary": "поиск на основании близости",
    "description": """
        Требует k в search_kwargs для поиска по близости.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_VECTOR_STORE_RETRIEVER_SIMILARITY,
}
#######

QUERY_WITH_VECTOR_STORE_RETRIEVER_MMR = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "vectorstore",
    "retriever_config": {
        "search_type": "mmr",
        "search_kwargs": {
            "k": 5,
            "fetch_k": 7,
        },
    },
    "stream": False,
}

QUERY_WITH_VECTOR_STORE_RETRIEVER_MMR_PAYLOAD = {
    "summary": "Поиск с mmr",
    "description": """
        Требуется k и fetch_k в search_kwargs для поддержки mmr в зависимости от векторной БД.
        search_type может быть similarity, mmr или similarity_score_threshold""",
    "value": QUERY_WITH_VECTOR_STORE_RETRIEVER_MMR,
}
#######

QUERY_WITH_VECTOR_STORE_RETRIEVER_SIMILARITY_SCORE = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "vectorstore",
    "retriever_config": {
        "search_type": "similarity_score_threshold",
        "search_kwargs": {"score_threshold": 0.7},
    },
    "stream": False,
}

QUERY_WITH_VECTOR_STORE_RETRIEVER_SIMILARITY_SCORE_PAYLOAD = {
    "summary": "Поиск с учетом порога по score",
    "description": """
        Требуется score_threshold: float (0~1) в search_kwargs.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_VECTOR_STORE_RETRIEVER_SIMILARITY_SCORE,
}
#######

QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "contexual-compression",
    "retriever_config": {
        "compressor_model_provider": "mixbread-ai",
        "compressor_model_name": "mixedbread-ai/mxbai-rerank-xsmall-v1",
        "top_k": 5,
        "search_type": "similarity",
        "search_kwargs": {"k": 10},
    },
    "stream": False,
}

QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_PAYLOAD = {
    "summary": "Поиск по близости + re-ranking",
    "description": """
        Требуется k в search_kwargs для поиска по близости.
        search_type может быть similarity, mmr или similarity_score_threshold.
        Поддерживается только при использовании reranker'а mixedbread-ai/mxbai-rerank-xsmall-v1.""",
    "value": QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER,
}
#####


QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_MMR = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "contexual-compression",
    "retriever_config": {
        "compressor_model_provider": "mixbread-ai",
        "compressor_model_name": "mixedbread-ai/mxbai-rerank-xsmall-v1",
        "top_k": 5,
        "search_type": "mmr",
        "search_kwargs": {
            "k": 10,
            "fetch_k": 30,
        },
    },
    "stream": False,
}

QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_MMR_PAYLOAD = {
    "summary": "mmr + re-ranking",
    "description": """
        Требуется k и fetch_k в search kwargs для mmr.
        search_type может быть similarity, mmr или similarity_score_threshold.
        Поддерживается только при использовании reranker'а mixedbread-ai/mxbai-rerank-xsmall-v1.""",
    "value": QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_MMR,
}

#####


QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_SIMILARITY_WITH_SCORE = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "contexual-compression",
    "retriever_config": {
        "compressor_model_provider": "mixbread-ai",
        "compressor_model_name": "mixedbread-ai/mxbai-rerank-xsmall-v1",
        "top_k": 5,
        "search_type": "similarity_score_threshold",
        "search_kwargs": {"score_threshold": 0.7},
    },
    "stream": False,
}

QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_SIMILARITY_WITH_SCORE_PAYLOAD = {
    "summary": "Порог по score + re-ranking",
    "description": """
        Требуется score_threshold: float (0~1) в search_kwargs для поиска по близости.
        search_type может быть similarity, mmr или similarity_score_threshold.
        Поддерживается только при использовании reranker'а mixedbread-ai/mxbai-rerank-xsmall-v1.""",
    "value": QUERY_WITH_CONTEXTUAL_COMPRESSION_RETRIEVER_SEARCH_TYPE_SIMILARITY_WITH_SCORE,
}

#####

QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "multi-query",
    "retriever_config": {
        "search_type": "similarity",
        "search_kwargs": {"k": 5},
        "retriever_llm_configuration": {
            "name": "openai-main/gpt-3-5-turbo",
            "provider": "truefoundry",
            "parameters": {"temperature": 0.9},
        },
    },
    "stream": False,
}

QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_PAYLOAD = {
    "summary": "multi-query + поиск по близости",
    "description": """
        Используется для сложных пользовательских запросов.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY,
}
#######


QUERY_WITH_MULTI_QUERY_RETRIEVER_MMR = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "multi-query",
    "retriever_config": {
        "search_type": "mmr",
        "search_kwargs": {
            "k": 5,
            "fetch_k": 10,
        },
        "retriever_llm_configuration": {
            "name": "openai-main/gpt-3-5-turbo",
            "provider": "truefoundry",
            "parameters": {"temperature": 0.9},
        },
    },
    "stream": False,
}

QUERY_WITH_MULTI_QUERY_RETRIEVER_MMR_PAYLOAD = {
    "summary": "multi-query + mmr",
    "description": """
        Требуется k и fetch_k в search_kwargs для mmr.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_MULTI_QUERY_RETRIEVER_MMR,
}
#######

QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "multi-query",
    "retriever_config": {
        "search_type": "similarity_score_threshold",
        "search_kwargs": {"score_threshold": 0.7},
        "retriever_llm_configuration": {
            "name": "openai-main/gpt-3-5-turbo",
            "provider": "truefoundry",
            "parameters": {"temperature": 0.9},
        },
    },
    "stream": False,
}

QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE_PAYLOAD = {
    "summary": "multi-query + порог по score",
    "description": """
        Обычно используется для сложных пользовательских запросов.
        Требуется score_threshold: float (0~1) в search kwargs.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE,
}
#######


QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_MMR = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "contexual-compression-multi-query",
    "retriever_config": {
        "compressor_model_provider": "mixbread-ai",
        "compressor_model_name": "mixedbread-ai/mxbai-rerank-xsmall-v1",
        "top_k": 5,
        "search_type": "mmr",
        "search_kwargs": {
            "k": 10,
            "fetch_k": 30,
        },
        "retriever_llm_configuration": {
            "name": "openai-main/gpt-3-5-turbo",
            "provider": "truefoundry",
            "parameters": {"temperature": 0.9},
        },
    },
    "stream": False,
}

QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_MMR_PAYLOAD = {
    "summary": "multi-query + re-ranking + mmr",
    "description": """
        Обычно используется для сложных пользовательских запросов.
        Требуется k и fetch_k в search_kwargs для mmr.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_MMR,
}
#######

QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "contexual-compression-multi-query",
    "retriever_config": {
        "compressor_model_provider": "mixbread-ai",
        "compressor_model_name": "mixedbread-ai/mxbai-rerank-xsmall-v1",
        "top_k": 5,
        "search_type": "similarity",
        "search_kwargs": {"k": 10},
        "retriever_llm_configuration": {
            "name": "openai-main/gpt-3-5-turbo",
            "provider": "truefoundry",
            "parameters": {"temperature": 0.1},
        },
    },
    "stream": False,
}

QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_PAYLOAD = {
    "summary": "multi-query + re-ranking + поиск по близости",
    "description": """
        Обычно используется для сложных пользовательских запросов.
        Требуется k в search_kwargs для поиска по близости.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY,
}
#######

QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE = {
    "collection_name": "example",
    "query": "Расскажи в деталях все виды ответственности, связанные с утечками персональных данных",
    "model_configuration": {
        "name": "openai-main/gpt-3-5-turbo",
        "provider": "truefoundry",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "contexual-compression-multi-query",
    "retriever_config": {
        "compressor_model_provider": "mixbread-ai",
        "compressor_model_name": "mixedbread-ai/mxbai-rerank-xsmall-v1",
        "top_k": 5,
        "search_type": "similarity_score_threshold",
        "search_kwargs": {"score_threshold": 0.7},
        "retriever_llm_configuration": {
            "name": "openai-main/gpt-3-5-turbo",
            "provider": "truefoundry",
            "parameters": {"temperature": 0.1},
        },
    },
    "stream": False,
}

QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE_PAYLOAD = {
    "summary": "multi-query + re-ranking + Порог по score",
    "description": """
        Обычно используется для сложных пользовательских запросов.
        Требуется k в search_kwargs для поиска по близости.
        search_type может быть similarity, mmr или similarity_score_threshold.""",
    "value": QUERY_WITH_CONTEXTUAL_COMPRESSION_MULTI_QUERY_RETRIEVER_SIMILARITY_SCORE,
}
#######
