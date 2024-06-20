from fastapi import APIRouter, Body, HTTPException

from backend.logger import logger
from backend.rag.api_routers.examples.answer import example_answer_payload
from backend.rag.query_controllers.example.controller import ExampleQueryController
from backend.rag.query_controllers.example.schemas import ExampleQueryInput, AnswerResultDto

router = APIRouter(
    prefix="/answer",
    tags=["answer"],
)


@router.post("/")
async def answer(
    request: ExampleQueryInput = Body(openapi_examples=example_answer_payload)
):  # -> AnswerResultDto:
    try:
        res = await ExampleQueryController.answer(request)
        return res
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))
