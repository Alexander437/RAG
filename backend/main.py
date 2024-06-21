import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.base_config import fastapi_users, auth_backend
from backend.auth.schemas import UserRead, UserCreate, UserUpdate
from backend.rag.api_routers.components import router as components_router
from backend.rag.api_routers.collection import router as collection_router
from backend.rag.api_routers.internal import router as internal_router
from backend.rag.api_routers.answer import router as answer_router

app = FastAPI(
    title="Интеллектуальный ассистент"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(components_router)
app.include_router(collection_router)
# Добавить валидацию gigachat и path_to_model для embeddings
app.include_router(internal_router)
app.include_router(answer_router)

# Cors - откуда разрешено отправлять запрос
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0")
