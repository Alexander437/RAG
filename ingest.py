import asyncio
import time

from backend.rag.metadata_store.client import METADATA_STORE_CLIENT
from backend.rag.schemas import IngestDataToCollectionDto
from backend.rag.indexer.indexer import ingest_data as ingest_data_to_collection


async def ingest(
        collection_name: str = "test",
        data_source_fqn: str = "localdir::/media/alex/Elements/My_projects/RAG/data"
):
    collection = METADATA_STORE_CLIENT.get_collection_by_name(collection_name, no_cache=True)

    data_source = METADATA_STORE_CLIENT.get_data_source_from_fqn(data_source_fqn)

    # Create a data ingestion request
    # It requires collection name & data source FQN
    request = IngestDataToCollectionDto(
        collection_name=collection.name,
        data_source_fqn=data_source.fqn,
    )

    await ingest_data_to_collection(request=request)


if __name__ == "__main__":
    start = time.time()
    # Run only when u have to ingest data
    print("Ingesting Data....")
    asyncio.run(ingest())

    end = time.time()
    print(f"Time taken to ingest data: {end-start} seconds")