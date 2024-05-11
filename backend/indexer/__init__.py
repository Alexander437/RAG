"""
Есть источник данных со старыми и новыми данными. `Indexer` используется для добавления
новых данных в коллекцию.

```bash
python3 backend/indexer/main.py --collection_name example_collction --data_source_fqn "tests/data_example/Постановление Правительства РФ от 16.03.2009 N 228 (ред. от.pdf" \
--data_ingestion_mode FULL
```
"""
from dotenv import load_dotenv

# load environment variables
load_dotenv()
