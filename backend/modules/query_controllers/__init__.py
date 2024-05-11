"""
Использование LLM для ответа на вопросы

Похоже, пока filter для metadata будет работать только с QdrantFilter

API:
```python
 # Streaming Client
import httpx
from httpx import Timeout

from backend.modules.query_controllers.example.types import ExampleQueryInput

payload = {
  "collection_name": "test",
  "query": "Какие преимущества у Diners club black metal edition?",
  "model_configuration": {
  "name": "openai-devtest/gpt-3-5-turbo",
    "parameters": {
      "temperature": 0.1
    },
    "provider": "truefoundry"
  },
  "prompt_template": "Answer the question based only on the following context:\nContext: {context} \nQuestion: {question}",
  "retriever_name": "vectorstore",
  "retriever_config": {
    "search_type": "similarity",
    "search_kwargs": {
      "k": 20
    },
    "filter": {}
  },
  "stream": True
}

data = ExampleQueryInput(**payload).dict()
ENDPOINT_URL = 'http://localhost:8000/retrievers/example-app/answer'


with httpx.stream('POST', ENDPOINT_URL, json=data, timeout=Timeout(5.0*60)) as r:
    for chunk in r.iter_text():
        print(chunk)
```
"""
from backend.modules.query_controllers.example.controller import ExampleQueryController
from backend.modules.query_controllers.query_controller import register_query_controller


register_query_controller("default", ExampleQueryController)
