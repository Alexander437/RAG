import time
import httpx
from httpx import Timeout

from backend.rag.query_controllers.example.schemas import ExampleQueryInput

payload = {
    "collection_name": "test",
    "query": "Что говорится в Конституции по поводу защиты информации?",
    "llm_configuration": {
        "name": "bambucha/saiga-llama3",
        "provider": "ollama",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос дайте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
    "retriever_name": "vectorstore",
    "retriever_config": {"search_type": "similarity", "search_kwargs": {"k": 5}},
    "stream": True,
}

payload = ExampleQueryInput(**payload).dict()
ENDPOINT_URL = 'http://localhost:8000/answer'

print("Start\n")
with httpx.stream('POST', ENDPOINT_URL, json=payload, timeout=Timeout(5.0*6000)) as r:
    time.sleep(60)
    for chunk in r.iter_text():
        print(chunk)
