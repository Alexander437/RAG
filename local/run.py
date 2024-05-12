import asyncio
import sys
sys.path.append("/media/alex/Elements/My_projects/RAG")

from backend.modules.query_controllers import ExampleQueryController
from backend.modules.query_controllers.example.types import ExampleQueryInput

# Payload for the query
# You can try different payload examples from `backend.modules.query_controllers.example.payload`
request = {
    "collection_name": "example",
    "query": "Расскажи про угрозы в области информационной безопасности",
    "model_configuration": {
        "name": "bambucha/saiga-llama3",
        "provider": "ollama",
        "parameters": {"temperature": 0.1},
    },
    "prompt_template": "Ответ на вопрос предоставьте, опираясь только на следующий контекст:\nКонтекст: {context} \nВопрос: {question}",
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

# Create a controller object
controller = ExampleQueryController()

# Get the answer
answer = asyncio.run(controller.answer(ExampleQueryInput(**request)))
print(f"Answer: {answer.get('answer')}")
# print(f"Docs: {answer.get('docs')}")
