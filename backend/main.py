import uvicorn
from fastapi import FastAPI

from backend.rag.api_routers.components import router as components_router
# from backend.rag.api_routers.collection import router as collection_router
from backend.rag.api_routers.internal import router as internal_router
from backend.rag.api_routers.answer import router as answer_router

app = FastAPI(
    title="Интеллектуальный ассистент, работающий по алгоритму RAG"
)


app.include_router(components_router)
# Нужно хранить сведения о коллекциях не в файле, а, например, в redis и исправить ingest_data в indexer
# app.include_router(collection_router)
# Добавить валидацию gigachat и path_to_model для embeddings
# app.include_router(internal_router)
# нужна схема выходных данных
app.include_router(answer_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
