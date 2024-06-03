import os
import tempfile
from typing import Dict, List

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from backend.constants import DATA_POINT_FQN_METADATA_KEY, DATA_POINT_HASH_METADATA_KEY
from backend.logger import logger
from backend.rag.dataloaders.loader import get_loader_for_data_source
from backend.rag.embedders.embedder import get_embedder
from backend.rag.indexer.schemas import DataIngestionConfig
from backend.rag.metadata_store.client import METADATA_STORE_CLIENT
from backend.rag.parsers.parser import get_parser_for_extension
from backend.rag.schemas import DataPointVector, DataIngestionRunStatus, DataIngestionMode, LoadedDataPoint, \
    IngestDataToCollectionDto, CreateDataIngestionRun
from backend.rag.vector_db.client import VECTOR_STORE_CLIENT
from backend.settings import settings


def get_data_point_fqn_to_hash_map(
    data_point_vectors: List[DataPointVector],
    ) -> Dict[str, str]:
    """
    Возвращает отображение из точки данных в hash
    """
    data_point_fqn_to_hash: Dict[str, str] = {}
    for data_point_vector in data_point_vectors:
        if data_point_vector.data_point_fqn not in data_point_fqn_to_hash:
            data_point_fqn_to_hash[data_point_vector.data_point_fqn] = data_point_vector.data_point_hash

    return data_point_fqn_to_hash


async def sync_data_source_to_collection(inputs: DataIngestionConfig):
    """
    Синхронизирует источник данных с коллекцией, выполняя шаги:
    1. Обновляет статус приема данных, чтобы указать, что извлекаются существующие векторы
    2. Извлекает существующие векторы точек данных из vectorstore
    3. Регистрирует общее количество существующих точек данных в коллекции
    4. Обновляет статус выполнения приема данных, чтобы показать, что прием данных начался
    5. Вызывает функцию _sync_data_source_to_collection для приема данных
    6. Обновляет статус выполнения приема данных, чтобы указать на завершение приема данных
    7. Если для приема данных выбран режим FULL, устаревшие векторы точек данных удаляются из vectorstore
    8. Обновляет статус выполнения приема данных, чтобы указать на завершение очистки данных.
    Args:
        inputs (DataIngestionConfig): Конфигурация приема данных
    Raises:
        Exception: Если во время приема данных или очистки данных возникает ошибка
    Returns:
        None
    """
    METADATA_STORE_CLIENT.update_data_ingestion_run_status(
        data_ingestion_run_name=inputs.data_ingestion_run_name,
        status=DataIngestionRunStatus.FETCHING_EXISTING_VECTORS,
    )
    try:
        existing_data_point_vectors = VECTOR_STORE_CLIENT.list_data_point_vectors(
            collection_name=inputs.collection_name,
            data_source_fqn=inputs.data_source.fqn,
        )
        previous_snapshot = get_data_point_fqn_to_hash_map(
            data_point_vectors=existing_data_point_vectors
        )

        logger.info(
            f"Total existing data point vectors in collection {inputs.collection_name}: {len(existing_data_point_vectors)}"
        )
    except Exception as e:
        logger.exception(e)
        METADATA_STORE_CLIENT.update_data_ingestion_run_status(
            data_ingestion_run_name=inputs.data_ingestion_run_name,
            status=DataIngestionRunStatus.FETCHING_EXISTING_VECTORS_FAILED,
        )
        raise e
    METADATA_STORE_CLIENT.update_data_ingestion_run_status(
        data_ingestion_run_name=inputs.data_ingestion_run_name,
        status=DataIngestionRunStatus.DATA_INGESTION_STARTED,
    )
    try:
        await _sync_data_source_to_collection(
            inputs=inputs,
            previous_snapshot=previous_snapshot,
        )
    except Exception as e:
        logger.exception(e)
        METADATA_STORE_CLIENT.update_data_ingestion_run_status(
            data_ingestion_run_name=inputs.data_ingestion_run_name,
            status=DataIngestionRunStatus.DATA_INGESTION_FAILED,
        )
        raise e
    METADATA_STORE_CLIENT.update_data_ingestion_run_status(
        data_ingestion_run_name=inputs.data_ingestion_run_name,
        status=DataIngestionRunStatus.DATA_INGESTION_COMPLETED,
    )
    # Delete the outdated data point vectors from the vector store
    if inputs.data_ingestion_mode == DataIngestionMode.FULL:
        METADATA_STORE_CLIENT.update_data_ingestion_run_status(
            data_ingestion_run_name=inputs.data_ingestion_run_name,
            status=DataIngestionRunStatus.DATA_CLEANUP_STARTED,
        )
        try:
            VECTOR_STORE_CLIENT.delete_data_point_vectors(
                collection_name=inputs.collection_name,
                data_point_vectors=existing_data_point_vectors,
            )
        except Exception as e:
            logger.exception(e)
            METADATA_STORE_CLIENT.update_data_ingestion_run_status(
                data_ingestion_run_name=inputs.data_ingestion_run_name,
                status=DataIngestionRunStatus.DATA_CLEANUP_FAILED,
            )
            raise e
    METADATA_STORE_CLIENT.update_data_ingestion_run_status(
        data_ingestion_run_name=inputs.data_ingestion_run_name,
        status=DataIngestionRunStatus.COMPLETED,
    )


async def _sync_data_source_to_collection(
    inputs: DataIngestionConfig, previous_snapshot: Dict[str, str] = None
):
    """
    Синхронизирует данные из источника данных с коллекцией.
    Args:
        inputs (DataIngestionConfig): Конфигурация для приема данных
        previous_snapshot (Dict[str, str], optional): Словарь сопоставляющий полные имена точек данных с их хэшами.
    Raises:
        Exception: Если не удалось принять какие-либо точки данных
    Returns:
        None
    """

    failed_data_point_fqns = []
    documents_ingested_count = 0
    # Create a temp dir to store the data
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Load the data from the source to the dest dir
        logger.info("Loading data from data source")
        data_source_loader = get_loader_for_data_source(inputs.data_source.type)
        loaded_data_points_batch_iterator = data_source_loader.load_filtered_data(
            data_source=inputs.data_source,
            dest_dir=tmpdirname,
            previous_snapshot=previous_snapshot,
            batch_size=inputs.batch_size,
            data_ingestion_mode=inputs.data_ingestion_mode,
        )

        for loaded_data_points_batch in loaded_data_points_batch_iterator:
            try:
                await ingest_data_points(
                    inputs=inputs,
                    loaded_data_points=loaded_data_points_batch,
                    documents_ingested_count=documents_ingested_count,
                )
                documents_ingested_count = documents_ingested_count + len(
                    loaded_data_points_batch
                )
            except Exception as e:
                logger.exception(e)
                if inputs.raise_error_on_failure:
                    raise e
                failed_data_point_fqns.extend(
                    [doc.data_point_fqn for doc in loaded_data_points_batch]
                )

        if len(failed_data_point_fqns) > 0:
            logger.error(
                f"Failed to ingest {len(failed_data_point_fqns)} data points. data point fqns:"
            )
            logger.error(failed_data_point_fqns)
            METADATA_STORE_CLIENT.log_errors_for_data_ingestion_run(
                data_ingestion_run_name=inputs.data_ingestion_run_name,
                errors={"failed_data_point_fqns": failed_data_point_fqns},
            )
            raise Exception(
                f"Failed to ingest {len(failed_data_point_fqns)} data points"
            )


async def ingest_data_points(inputs: DataIngestionConfig,
                             loaded_data_points: List[LoadedDataPoint],
                             documents_ingested_count: int):
    """
    Принимает точки данных в векторное хранилище для данного батча.
    Args:
        inputs (DataIngestionConfig): Конфигурация приема данных
        loaded_data_points (List[LoadedDataPoint]): Список загруженных точек данных для приема
        documents_ingested_count (int): Количество уже принятых документов
    Returns:
        None: Если в данном пакете не найдены документы для индексации.
    Raises:
        None
    """

    embeddings = get_embedder(
        embedder_config=inputs.embedder_config,
    )
    documents_to_be_upserted = []
    logger.info(
        f"Processing {len(loaded_data_points)} new documents and completed: {documents_ingested_count}"
    )
    for index, loaded_data_point in enumerate(loaded_data_points):
        logger.info(
            f"[{index+1}/{len(loaded_data_points)}/{documents_ingested_count}] Parsing [{index+1}/{len(loaded_data_points)}] new document"
        )
        # Get parser for required file extension
        parser = get_parser_for_extension(
            file_extension=loaded_data_point.file_extension,
            parsers_map=inputs.parser_config.parse_map,
            max_chunk_size=inputs.parser_config.chunk_size,
            chunk_overlap=inputs.parser_config.chunk_overlap,
        )
        if parser is None:
            logger.warning(
                f"Could not parse data point {loaded_data_point.data_point_fqn} as no parser found for file extension: {loaded_data_point.file_extension}"
            )
            continue
        # chunk the given document
        chunks = await parser.get_chunks(
            filepath=loaded_data_point.local_filepath,
            metadata=loaded_data_point.metadata,
        )
        # Update data source metadata
        for chunk in chunks:
            if loaded_data_point.metadata:
                chunk.metadata.update(loaded_data_point.metadata)
            # Most importantly, update the metadata with data point fqn and hash
            chunk.metadata.update(
                {
                    f"{DATA_POINT_FQN_METADATA_KEY}": loaded_data_point.data_point_fqn,
                    f"{DATA_POINT_HASH_METADATA_KEY}": loaded_data_point.data_point_hash,
                }
            )
            documents_to_be_upserted.append(chunk)
        logger.info("%s -> %s chunks", loaded_data_point.local_filepath, len(chunks))

        # delete the file from temp dir after processing
        try:
            if loaded_data_point.local_filepath:
                os.remove(loaded_data_point.local_filepath)
                print(
                    f"Processing done! Deleting file {loaded_data_point.local_filepath}"
                )
                logger.debug(
                    f"Processing done! Deleting file {loaded_data_point.local_filepath}"
                )
        except Exception as e:
            print(
                f"Failed to delete file {loaded_data_point.local_filepath} after processing. Error: {e}"
            )
            logger.error(
                f"Failed to delete file {loaded_data_point.local_filepath} after processing. Error: {e}"
            )

    docs_to_index_count = len(documents_to_be_upserted)
    if docs_to_index_count == 0:
        logger.warning(
            "No documents found to index in given batch. Moving to next batch..."
        )
        return
    logger.info(
        f"Upserting {docs_to_index_count} documents to vector store for given batch"
    )
    # Upserted all the documents_to_be_ingested
    VECTOR_STORE_CLIENT.upsert_documents(
        collection_name=inputs.collection_name,
        documents=documents_to_be_upserted,
        embeddings=embeddings,
        incremental=inputs.data_ingestion_mode == DataIngestionMode.INCREMENTAL,
    )


async def ingest_data(request: IngestDataToCollectionDto):
    """Прием данных в коллекцию (при работе с сайтом)"""
    try:
        collection = METADATA_STORE_CLIENT.get_collection_by_name(
            collection_name=request.collection_name, no_cache=True
        )
        if not collection:
            logger.error(
                f"Collection with name {request.collection_name} does not exist."
            )
            raise HTTPException(
                status_code=404,
                detail=f"Collection with name {request.collection_name} does not exist.",
            )

        if not collection.associated_data_sources:
            logger.error(
                f"Collection {request.collection_name} does not have any associated data sources."
            )
            raise HTTPException(
                status_code=400,
                detail=f"Collection {request.collection_name} does not have any associated data sources.",
            )
        associated_data_sources_to_be_ingested = []
        if request.data_source_fqn:
            associated_data_sources_to_be_ingested = [
                collection.associated_data_sources.get(request.data_source_fqn)
            ]
        else:
            associated_data_sources_to_be_ingested = (
                collection.associated_data_sources.values()
            )

        for associated_data_source in associated_data_sources_to_be_ingested:
            logger.debug(
                f"Starting ingestion for data source fqn: {associated_data_source.data_source_fqn}"
            )
            data_ingestion_run = CreateDataIngestionRun(
                collection_name=collection.name,
                data_source_fqn=associated_data_source.data_source_fqn,
                embedder_config=collection.embedder_config,
                parser_config=associated_data_source.parser_config,
                data_ingestion_mode=request.data_ingestion_mode,
                raise_error_on_failure=request.raise_error_on_failure,
            )
            created_data_ingestion_run = (
                METADATA_STORE_CLIENT.create_data_ingestion_run(
                    data_ingestion_run=data_ingestion_run
                )
            )
            await sync_data_source_to_collection(
                inputs=DataIngestionConfig(
                    collection_name=created_data_ingestion_run.collection_name,
                    data_ingestion_run_name=created_data_ingestion_run.name,
                    data_source=associated_data_source.data_source,
                    embedder_config=collection.embedder_config,
                    parser_config=created_data_ingestion_run.parser_config,
                    data_ingestion_mode=created_data_ingestion_run.data_ingestion_mode,
                    raise_error_on_failure=created_data_ingestion_run.raise_error_on_failure,
                )
            )
            created_data_ingestion_run.status = DataIngestionRunStatus.COMPLETED
        return JSONResponse(
            status_code=201,
            content={"message": "triggered"},
        )
    except HTTPException as exp:
        raise exp
    except Exception as exp:
        logger.exception(exp)
        raise HTTPException(status_code=500, detail=str(exp))