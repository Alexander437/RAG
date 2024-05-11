"""
После поиска документов (например, полнотекстового) позволяет переранжировать их и выбрать k на основании запроса

API:
```python
from backend.modules.reranker import MxBaiReranker
reranker = MxBaiReranker(model="mixedbread-ai/mxbai-rerank-base-v1", top_k=3)  # mxbai-rerank-large-v1
# ...
res = parser.get_chunks("tests/data_example/Постановление Правительства РФ от 16.03.2009 N 228 (ред. от.pdf", metadata=dict())
doc = asyncio.run(res)
reranker.compress_documents(doc, query="Финансовое обеспечение расходов на содержание")
```
"""
from backend.modules.reranker.mxbai_reranker import MxBaiReranker
