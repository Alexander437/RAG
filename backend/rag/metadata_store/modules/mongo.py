import uuid
from typing import List, Union, Dict, Any

from pymongo import MongoClient
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError

from backend.logger import logger
from backend.rag.metadata_store.base import BaseMetadataStore
from backend.rag.schemas import CreateCollection, Collection, CreateDataSource, DataSource, CreateDataIngestionRun, \
    DataIngestionRun, AssociateDataSourceWithCollection, DataIngestionRunStatus


class MongoMetadataStore(BaseMetadataStore):
    def __init__(self, config: dict):
        db = MongoClient(config["url"])[config["db"]]
        try:
            _ = db.list_collection_names()
        except ServerSelectionTimeoutError as e:
            raise ValueError('Mongodb server unavailable')
        self.collections = db["collections"]
        self.data_sources = db["data_sources"]
        self.runs = db["runs"]

    def create_collection(self, collection: CreateCollection) -> Collection:
        logger.debug(f"[Metadata Store] Creating collection {collection.name}")
        existing_collection = self.collections.find_one({"_id": collection.name})
        if existing_collection is not None:
            logger.error(
                f"[Metadata Store] Existing collection found with name {collection.name}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Collection with name {collection.name} already exists.",
            )
        self.collections.insert_one({
            "_id": collection.name,
            "name": collection.name,
            "description": collection.description,
            "embedder_config": collection.embedder_config.dict(),
            "associated_data_sources": {}
        })
        return Collection(associated_data_sources={}, **collection.dict())

    def get_collection_by_name(
        self, collection_name: str, no_cache: bool = True
    ) -> Collection | None:
        data = self.collections.find_one({"_id": collection_name})
        if data is not None:
            return Collection(**data)
        else:
            return None

    def get_collections(
        self,
    ) -> List[Collection]:
        return [Collection(**data) for data in self.collections.find()]

    def create_data_source(self, data_source: CreateDataSource) -> DataSource:
        existing_data_source = self.data_sources.find_one({"_id": data_source.fqn()})
        if existing_data_source is not None:
            logger.error(
                f"[Metadata Store] Existing data_source found with FQN {data_source.fqn()}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Data_source with FQN {data_source.fqn()} already exists.",
            )
        d = {"_id": data_source.fqn()}
        d.update(data_source.dict())
        self.data_sources.insert_one(d)
        return DataSource(**data_source.dict())

    def get_data_source_from_fqn(self, fqn: str) -> Union[DataSource, None]:
        data = self.data_sources.find_one({"_id": fqn})
        if data is not None:
            return DataSource(**data)
        else:
            return None

    def get_data_sources(self) -> List[DataSource]:
        return [DataSource(**data) for data in self.data_sources.find()]

    def create_data_ingestion_run(
        self, data_ingestion_run: CreateDataIngestionRun
    ) -> DataIngestionRun:
        name = str(uuid.uuid1())
        d = {
            "_id": name,
            "name": name,
            "status": DataIngestionRunStatus.INITIALIZED
        }
        d.update(data_ingestion_run.dict())
        self.runs.insert_one(d)
        return DataIngestionRun(**d)

    def get_data_ingestion_run(
        self, data_ingestion_run_name: str, no_cache: bool = False
    ) -> Union[DataIngestionRun, None]:
        data = self.runs.find_one({"_id": data_ingestion_run_name})
        if data is not None:
            return DataIngestionRun(**data)
        else:
            return None

    def get_data_ingestion_runs(
        self, collection_name: str, data_source_fqn: str = None
    ) -> List[DataIngestionRun]:
        return [DataIngestionRun(**data) for data in self.runs.find()]

    def delete_collection(self, collection_name: str, include_runs=False):
        self.collections.delete_one({"_id": collection_name})
        if include_runs:
            self.runs.delete_many({"collection_name": collection_name})

    def associate_data_source_with_collection(
        self,
        collection_name: str,
        data_source_association: AssociateDataSourceWithCollection,
    ) -> Collection:

        collection_dict = self.collections.find_one({"_id": collection_name})
        data_source_association_dict = data_source_association.dict()
        fqn_l = data_source_association.data_source_fqn.split("::")
        data_source_association_dict.update({
            "data_source": {
                "type": fqn_l[0],
                "uri": fqn_l[1],
                "metadata": None
            }
        })
        collection_dict["associated_data_sources"].update(
            {data_source_association.data_source_fqn: data_source_association_dict}
        )
        self.collections.update_one(
            {"_id": collection_name},
            {"$set": {"associated_data_sources": collection_dict["associated_data_sources"]}}
        )
        return Collection(**collection_dict)

    def unassociate_data_source_with_collection(
        self,
        collection_name: str,
        data_source_fqn: str,
    ) -> Collection:
        collection_dict = self.collections.find_one({"_id": collection_name})
        collection_dict["associated_data_sources"].pop(data_source_fqn, None)
        self.collections.update_one(
            {"_id": collection_name},
            {"$set": {"associated_data_sources": collection_dict["associated_data_sources"]}}
        )
        return Collection(**collection_dict)

    def update_data_ingestion_run_status(
        self,
        data_ingestion_run_name: str,
        status: DataIngestionRunStatus,
    ):
        self.runs.update_one({"_id": data_ingestion_run_name}, {"$set": {"status": status}})

    def log_metrics_for_data_ingestion_run(
        self,
        data_ingestion_run_name: str,
        metric_dict: dict[str, int | float],
        step: int = 0,
    ):
        logger.info(f"Logging metrics for data ingestion run {data_ingestion_run_name}")
        logger.info(f"step: {step}, metric_dict: {metric_dict}")

    def log_errors_for_data_ingestion_run(
        self, data_ingestion_run_name: str, errors: Dict[str, Any]
    ):
        logger.info(f"Logging errors for data ingestion run {data_ingestion_run_name}")
        logger.info(f"errors: {errors}")
