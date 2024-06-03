"""
Хранит информацию о текущих действиях в коллекциях
и работа с коллекциями.

provider="local" -> хранение метаданных в .yaml файле, только одна коллекция!

API:
Для "local" нужно создать файл `./volumes/backend/metadata.yml` и заполнить его:
```yaml
collection_name: example
data_source:
  type: localdir
  uri: data/
parser_config:
  chunk_size: 1000
  parse_map:
    ".pdf": PdfParserFast
    ".md": MarkdownParser
embedder_config:
  provider: huggingface
  config:
    model_name: "/media/alex/Elements/My_projects/egeon/nn/lc-elastic/models/embeddings/distiluse-base-multilingual-cased-v1"
```

```python
import asyncio

from backend.modules.metadata_store.client import METADATA_STORE_CLIENT
from backend.types import DataIngestionRunStatus, CreateDataIngestionRun
from backend.indexer.types import DataIngestionConfig
from backend.indexer.indexer import sync_data_source_to_collection

collection = METADATA_STORE_CLIENT.get_collection_by_name(
    "example", no_cache=True
)

data_source = METADATA_STORE_CLIENT.get_data_source_from_fqn(fqn="tests/data_example/Постановление Правительства РФ от 16.03.2009 N 228.pdf")
associated_data_source = collection.associated_data_sources.get(data_source.fqn)

METADATA_STORE_CLIENT.update_data_ingestion_run_status(
data_ingestion_run_name="first data_ingestion",
status=DataIngestionRunStatus.DATA_INGESTION_STARTED,
)

data_ingestion_run = CreateDataIngestionRun(
    collection_name=collection.name,
    data_source_fqn=associated_data_source.data_source_fqn,
    embedder_config=collection.embedder_config,
    parser_config=associated_data_source.parser_config,
    data_ingestion_mode="FULL",
    raise_error_on_failure=True,
)
created_data_ingestion_run = METADATA_STORE_CLIENT.create_data_ingestion_run(
    data_ingestion_run=data_ingestion_run
)

inputs = DataIngestionConfig(
    collection_name=collection.name,
    data_ingestion_run_name=created_data_ingestion_run.name,
    data_source=data_source,
    embedder_config=collection.embedder_config,
    parser_config=created_data_ingestion_run.parser_config,
    data_ingestion_mode=created_data_ingestion_run.data_ingestion_mode,
    raise_error_on_failture=created_data_ingestion_run.raise_error_on_failure,
    batch_size=100,
)

asyncio.run(sync_data_source_to_collection(inputs=inputs))
```
"""
from backend.rag.metadata_store.base import register_metadata_store
from backend.rag.metadata_store.modules.local import LocalMetadataStore
from backend.rag.metadata_store.modules.mongo import MongoMetadataStore
from backend.settings import settings

# if settings.LOCAL:
register_metadata_store("file", LocalMetadataStore)
register_metadata_store("mongo", MongoMetadataStore)
