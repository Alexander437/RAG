"""
Код для работы с векторными БД

API:
```python
from backend.modules.vector_db.client import VECTOR_STORE_CLIENT
VECTOR_STORE_CLIENT.get_collections()
# ...
```
```python
from backend.modules.vector_db.qdrant import QdrantVectorDB
from backend.settings import settings

db = QdrantVectorDB(settings.VECTOR_DB_CONFIG)
# ...
embedder = get_embedder(embedder_config)
db.create_collection("example_collection", embedder)
db.get_collections()
client = db.get_vector_client()
# ...
res = parser.get_chunks("tests/data_example/Постановление Правительства РФ от 16.03.2009 N 228 (ред. от.pdf", metadata=dict())
doc = asyncio.run(res)
db.upsert_documents("example_collection", doc, embedder)
# ? как читать, но в GUI видно, что вставились
```
"""
from backend.modules.vector_db.base import BaseVectorDB
from backend.modules.vector_db.qdrant import QdrantVectorDB
from backend.modules.vector_db.singlestore import SingleStoreVectorDB
from backend.types import VectorDBConfig

SUPPORTED_VECTOR_DBS = {
    "qdrant": QdrantVectorDB,
    "singlestore": SingleStoreVectorDB,
}


def get_vector_db_client(config: VectorDBConfig) -> BaseVectorDB:
    if config.provider in SUPPORTED_VECTOR_DBS:
        return SUPPORTED_VECTOR_DBS[config.provider](config=config)
    else:
        raise ValueError(f"Unknown vector db provider: {config.provider}")
