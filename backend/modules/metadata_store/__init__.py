from backend.modules.metadata_store.base import register_metadata_store
from backend.modules.metadata_store.local import LocalMetadataStore
from backend.settings import settings

if settings.LOCAL:
    register_metadata_store("local", LocalMetadataStore)
