"""
Нужны для перемещения данных из источника (веб страница, файл) в файл.
* `WebLoader` скачивает в папку `/tmp/webloader`, определяемую `DEFAULT_BASE_DIR`

API:
```python
from backend.modules.dataloaders.loader import get_loader_for_data_source
from backend.types import DataSource, DataIngestionMode

dataloader = get_loader_for_data_source("localdir")
data_point_iter = dataloader.load_filtered_data(
            data_source=DataSource(uri="tests/data_example", type="example_type"),
            dest_dir="tests/data_example1",
            previous_snapshot={},
            batch_size=100,
            data_ingestion_mode=DataIngestionMode.FULL
        )
next(data_point_iter)  # будет возвращен объект `LoadedDataPoint`, а батч записан в dest_dir
```
"""
from backend.modules.dataloaders.webloader import WebLoader
from backend.modules.dataloaders.localdirloader import LocalDirLoader
from backend.modules.dataloaders.loader import register_dataloader
# from backend.settings import settings

register_dataloader("localdir", LocalDirLoader)
register_dataloader("web", WebLoader)
