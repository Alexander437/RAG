"""
Возвращают объекты `Embeddings` из LangChain
Можно кэшировать embeddings, чтобы избежать их повторного вычисления
с помощью `CacheBackedEmbeddings`, но пока, кажется, что в данном
случае это не полезно.

API:
```python
from backend.rag.embedders.embedder import get_embedder
from backend.rag.schemas import EmbedderConfig

config = {"model_name": "/media/alex/Elements/My_projects/egeon/nn/lc-elastic/models/embeddings/distiluse-base-multilingual-cased-v1"}
embedder_config = EmbedderConfig(provider="local", config=config)
embedder = get_embedder(embedder_config)
# И затем можно делать embedder.embed_documents(["document", "document1"])...
# или передать embedder в vectorstore
```
"""
from backend.rag.embedders.embedder import register_embedder
from backend.settings import settings

if settings.GIGACHAT_API_KEY:
    from langchain_community.embeddings.gigachat import GigaChatEmbeddings
    register_embedder("gigachat", GigaChatEmbeddings)

if settings.LOCAL:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    register_embedder("local", HuggingFaceEmbeddings)
