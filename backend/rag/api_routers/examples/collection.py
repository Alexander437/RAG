EMBEDDER_CONFIG = {
    "provider": "local",
    "config": {
        "model_name": "/media/alex/Elements/My_projects/egeon/nn/lc-elastic/models/embeddings/distiluse-base-multilingual-cased-v1"
    }
}
PARSER_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 0,
    "parse_map": {
        ".md": "MarkdownParser",
        ".pdf": "PdfParserFast"
    }
}
ASSOCIATED_DATA_SOURCE_LOCALDIR = {
    "data_source_fqn": "localdir::/media/alex/Elements/My_projects/RAG/data",
    "parser_config": PARSER_CONFIG,
}

example_create_collection = {
    "example": {
        "summary": "Создание коллекции с localdir",
        "description": """
            Требуется указывать абсолютный путь к директории""",
        "value": {
            "name": "test",
            "description": "Collection for test api",
            "embedder_config": EMBEDDER_CONFIG,
            "associated_data_sources": [ASSOCIATED_DATA_SOURCE_LOCALDIR]
            },
    }
}

example_associate_data_source = {
    "example": {
        "summary": "Добавление localdir-источника данных",
        "description": """
            Требуется указывать абсолютный путь к директории""",
        "value": {
            "data_source_fqn": "localdir::/media/alex/Elements/My_projects/RAG/data",
            "parser_config": PARSER_CONFIG,
            "collection_name": "test",
        },
    }
}

example_unassociate_data_source = {
    "example": {
        "summary": "Отключение источника данных",
        "description": "",
        "value": {
            "collection_name": "test",
            "data_source_fqn": "localdir::/media/alex/Elements/My_projects/RAG/data",
        },
    }
}

example_ingest = {
    "example": {
        "summary": "Начать прием данных",
        "description": "",
        "value": {
            "collection_name": "test",
            "data_source_fqn": "localdir::/media/alex/Elements/My_projects/RAG/data",
            "raise_error_on_failure": True,
            "batch_size": 100,
        },
    }
}

example_runs_list = {
    "example": {
        "summary": "Список задач приема данных",
        "description": "",
        "value": {
            "collection_name": "test",
            "data_source_fqn": "localdir::/media/alex/Elements/My_projects/RAG/data",
        },
    }
}
