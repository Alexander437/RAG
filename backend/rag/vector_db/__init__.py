"""
Код для работы с векторными БД

API:
```python
from backend.rag.vector_db.client import VECTOR_STORE_CLIENT
VECTOR_STORE_CLIENT.get_collections()
# ...
```
```python
from backend.rag.vector_db.modules.qdrant import QdrantVectorDB
from backend.settings import settings

db = QdrantVectorDB(settings.VECTOR_DB_CONFIG)
# ...
embedder = get_embedder(embedder_config)
db.create_collection("example", embedder)
db.get_collections()
client = db.get_vector_client()
# ...
res = parser.get_chunks("data/Постановление Правительства РФ от 16.03.2009 N 228.pdf", metadata=dict())
doc = asyncio.run(res)
db.upsert_documents("example", doc, embedder)
# в GUI видно, что вставились
```
"""
from backend.rag.vector_db.base import BaseVectorDB
from backend.rag.vector_db.modules.qdrant import QdrantVectorDB
from backend.rag.schemas import VectorDBConfig

SUPPORTED_VECTOR_DBS = {
    "qdrant": QdrantVectorDB,
}


def get_vector_db_client(config: VectorDBConfig) -> BaseVectorDB:
    if config.provider in SUPPORTED_VECTOR_DBS:
        return SUPPORTED_VECTOR_DBS[config.provider](config=config.config)
    else:
        raise ValueError(f"Unknown vector db provider: {config.provider}")
