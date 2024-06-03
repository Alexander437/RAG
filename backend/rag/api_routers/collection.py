from typing import Dict, List
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse

from backend.logger import logger
from backend.rag.api_routers.examples.collection import example_create_collection, example_associate_data_source, \
    example_unassociate_data_source, example_ingest, example_runs_list
from backend.rag.embedders.embedder import get_embedder
from backend.rag.metadata_store.client import METADATA_STORE_CLIENT
from backend.rag.indexer.indexer import ingest_data as ingest_data_to_collection
from backend.rag.schemas import CreateCollectionDto, Collection, CreateCollection, AssociateDataSourceWithCollection, \
    AssociateDataSourceWithCollectionDto, UnassociateDataSourceWithCollectionDto, IngestDataToCollectionDto, \
    ListDataIngestionRunsDto
from backend.rag.vector_db.client import VECTOR_STORE_CLIENT

router = APIRouter(
    prefix="/collections",
    tags=["collections"],
)


@router.get("/")
def get_collections() -> Dict[str, List[Collection]]:
    try:
        logger.debug("Listing all collections...")
        collections = METADATA_STORE_CLIENT.get_collections()
        if collections is None:
            return {"collections": []}
        return {"collections": [obj.dict() for obj in collections]}
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))


@router.post("/")
def create_collection(
        collection: CreateCollectionDto = Body(openapi_examples=example_create_collection)
) -> Dict[str, Collection]:
    try:
        logger.debug(f"Creating collection {collection.name}...")
        created_collection = METADATA_STORE_CLIENT.create_collection(
            collection=CreateCollection(
                name=collection.name,
                description=collection.description,
                embedder_config=collection.embedder_config,
            )
        )
        VECTOR_STORE_CLIENT.create_collection(
            collection_name=collection.name,
            embeddings=get_embedder(collection.embedder_config),
        )
        if collection.associated_data_sources:
            for data_source in collection.associated_data_sources:
                METADATA_STORE_CLIENT.associate_data_source_with_collection(
                    collection_name=created_collection.name,
                    data_source_association=AssociateDataSourceWithCollection(
                        data_source_fqn=data_source.data_source_fqn,
                        parser_config=data_source.parser_config,
                    ),
                )
            created_collection = METADATA_STORE_CLIENT.get_collection_by_name(
                collection_name=created_collection.name
            )
        return {"collection": created_collection.dict()}
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))


# Не работает для localdir
@router.post("/associate_data_source")
async def associate_data_source_to_collection(
        request: AssociateDataSourceWithCollectionDto = Body(openapi_examples=example_associate_data_source)
) -> Dict[str, Collection]:
    """Добавление источника данных для коллекции"""
    try:
        collection = METADATA_STORE_CLIENT.associate_data_source_with_collection(
            collection_name=request.collection_name,
            data_source_association=AssociateDataSourceWithCollection(
                data_source_fqn=request.data_source_fqn,
                parser_config=request.parser_config,
            ),
        )
        return {"collection": collection.dict()}
    except HTTPException as exp:
        raise exp
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))


# Не работает для localdir
@router.post("/unassociate_data_source")
async def unassociate_data_source_from_collection(
        request: UnassociateDataSourceWithCollectionDto = Body(openapi_examples=example_unassociate_data_source)
) -> Dict[str, Collection]:
    """Удаление источника данных из коллекции"""
    try:
        collection = METADATA_STORE_CLIENT.unassociate_data_source_with_collection(
            collection_name=request.collection_name,
            data_source_fqn=request.data_source_fqn,
        )
        return {"collection": collection.dict()}
    except HTTPException as exp:
        raise exp
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))


@router.post("/ingest")
async def ingest_data(
        request: IngestDataToCollectionDto = Body(openapi_examples=example_ingest)
) -> JSONResponse:
    """Прием данных в коллекцию"""
    try:
        return await ingest_data_to_collection(request)
    except HTTPException as exp:
        raise exp
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))


@router.delete("/{collection_name}")
def delete_collection(collection_name: str) -> Dict[str, bool]:
    """Удалить коллекцию по имени"""
    try:
        VECTOR_STORE_CLIENT.delete_collection(collection_name=collection_name)
        METADATA_STORE_CLIENT.delete_collection(collection_name, include_runs=True)
        return {"deleted": True}
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))


@router.post("/data_ingestion_runs/list")
def list_data_ingestion_runs(
        request: ListDataIngestionRunsDto = Body(openapi_examples=example_runs_list)
) -> Dict[str, list]:
    data_ingestion_runs = METADATA_STORE_CLIENT.get_data_ingestion_runs(
        request.collection_name, request.data_source_fqn
    )
    return {"data_ingestion_runs": [obj.dict() for obj in data_ingestion_runs]}


@router.get("/data_ingestion_runs/{data_ingestion_run_name}/status")
def get_collection_status(
        data_ingestion_run_name: str) -> Dict[str, str]:
    """Возвращает статус задачи получения данных"""
    data_ingestion_run = METADATA_STORE_CLIENT.get_data_ingestion_run(
        data_ingestion_run_name=data_ingestion_run_name, no_cache=True
    )

    if data_ingestion_run is None:
        raise HTTPException(
            status_code=404,
            detail=f"Data ingestion run {data_ingestion_run_name} not found"
        )

    return {
        "status": data_ingestion_run.status.value,
        "message": f"Data ingestion job run {data_ingestion_run.name} in {data_ingestion_run.status.value}. Check logs for more details.",
    }
