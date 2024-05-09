"""
Возвращают объекты `Embeddings` из LangChain
Можно кэшировать embeddings, чтобы избежать их повторного вычисления
с помощью `CacheBackedEmbeddings`, но пока, кажется, что в данном
случае это не полезно.

API:
```python
from backend.modules.embedders.embedder import get_embedder
from backend.types import EmbedderConfig

config = {"model_name": "/media/alex/Elements/My_projects/egeon/nn/lc-elastic/models/embeddings/distiluse-base-multilingual-cased-v1"}
embedder_config = EmbedderConfig(provider="huggingface", config=config)
embedder = get_embedder(embedder_config)  # И затем можно делать embedder.embed_document(["document", "document1"])...
# или передать embedder в vectorstore
```
"""
from backend.modules.embedders.embedder import register_embedder
from backend.settings import settings

if settings.GIGACHAT_API_KEY:
    from langchain_community.embeddings.gigachat import GigaChatEmbeddings
    register_embedder("gigachat", GigaChatEmbeddings)

if settings.LOCAL:
    # from backend.modules.embedders.mixbread_embedder import MixBreadEmbeddings
    # register_embedder("mixedbread", MixBreadEmbeddings)
    from langchain_community.embeddings import HuggingFaceEmbeddings
    register_embedder("huggingface", HuggingFaceEmbeddings)