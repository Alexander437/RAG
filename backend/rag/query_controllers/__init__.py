# рядом с search_type можно указать filter для qdrant
"""
Использование LLM для ответа на вопросы
API:
```python
import asyncio

from backend.rag.query_controllers import ExampleQueryController
from backend.rag.query_controllers.example.schemas import ExampleQueryInput

# You can try different payload examples from `backend.modules.query_controllers.example.payload`
request = {
    "collection_name": "example",
    "query": "Какие нормативно-правовые документы регламентируют политику в области связи?",
    "llm_configuration": {
        "name": "bambucha/saiga-llama3",
        "provider": "ollama",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "vectorstore",
    "retriever_config": {
        "search_type": "similarity",
        "search_kwargs": {
            "k": 5,
        },
    },
    "stream": False,
}
# You can change the query here
# print(f"Payload: {request}")

# Get the answer
answer = asyncio.run(ExampleQueryController.answer(ExampleQueryInput(**request)))

print(f"Answer: {answer.get('answer')}")
# print(f"Docs: {answer.get('docs')}")
```
"""
from backend.rag.query_controllers.example.controller import ExampleQueryController
from backend.rag.query_controllers.query_controller import register_query_controller


register_query_controller("default", ExampleQueryController)
