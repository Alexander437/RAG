"""
Нужны для перемещения данных из источника (веб страница, файл) в файл.
* `WebLoader` скачивает в папку `/tmp/webloader`, определяемую `DEFAULT_BASE_DIR`

API:
```python
from backend.rag.dataloaders.loader import get_loader_for_data_source
from backend.rag.schemas import DataSource, DataIngestionMode

dataloader = get_loader_for_data_source("localdir")
data_point_iter = dataloader.load_filtered_data(
            data_source=DataSource(uri="data", type="example_type", metadata={}),
            dest_dir="data/example",
            previous_snapshot={},
            batch_size=100,
            data_ingestion_mode=DataIngestionMode.FULL
        )
next(data_point_iter)  # будет возвращен объект `LoadedDataPoint`, а батч записан в dest_dir
```
"""
from backend.rag.dataloaders.modules.webloader import WebLoader
from backend.rag.dataloaders.modules.localdirloader import LocalDirLoader
from backend.rag.dataloaders.loader import register_dataloader
# from backend.settings.py import settings.py

register_dataloader("localdir", LocalDirLoader)
register_dataloader("web", WebLoader)
