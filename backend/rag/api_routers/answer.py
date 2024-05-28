from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException
from langchain_core.documents import Document

from backend.logger import logger
from backend.rag.query_controllers.example.controller import EXAMPLES, ExampleQueryController
from backend.rag.query_controllers.example.schemas import ExampleQueryInput, AnswerResultDto

router = APIRouter(
    prefix="/answer",
    tags=["answer"],
)


@router.post("/")
async def answer(
    request: ExampleQueryInput = Body(openapi_examples=EXAMPLES)
) -> AnswerResultDto:
    try:
        res = await ExampleQueryController.answer(request)
        return res
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=AnswerResultDto(answer="", docs=[]))
