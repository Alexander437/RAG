import argparse
from typing import Optional

from pydantic import BaseModel

from backend.constants import DEFAULT_BATCH_SIZE
from backend.types import DataIngestionMode


class ParsedIndexingArguments(BaseModel):
    """
    Конфигурация для хранения аргументов индексирования.
    Требуется имя коллекции (существующей) и полное имя источника данных
    """
    collection_name: str
    data_source_fqn: str
    data_ingestion_run_name: Optional[str] = None
    data_ingestion_mode: DataIngestionMode
    raise_error_on_failure: bool
    batch_size: int = DEFAULT_BATCH_SIZE


def parse_args() -> ParsedIndexingArguments:
    parser = argparse.ArgumentParser(
        prog="train",
        usage="%(prog)s [options]",
        description="Задача индексации для разбиения документов на части и индексации в VectorDB",
        formatter_class=argparse.MetavarTypeHelpFormatter,
    )
    parser.add_argument(
        "--collection_name",
        type=str,
        required=True,
        help="уникальное имя для коллекции",
    )
    parser.add_argument(
        "--data_source_fqn",
        type=str,
        required=True,
        help="полное имя для источника данных",
    )
    parser.add_argument(
        "--data_ingestion_run_name",
        type=str,
        required=False,
        default=None,
        help="уникальное имя для процесса приема данных",
    )
    parser.add_argument(
        "--data_ingestion_mode",
        type=str,
        required=False,
        default="INCREMENTAL",
        help="Режим приема данных. NONE/INCREMENTAL/FULL",
    )
    parser.add_argument(
        "--raise_error_on_failure",
        type=str,
        required=False,
        default="True",
        help="Если true, то генерируется исключение при обработке батча, иначе процесс продолжается для других батчей",
    )
    parser.add_argument(
        "--batch_size",
        type=str,
        required=False,
        default="100",
        help="Размер батча для обрабатываемых документов",
    )
    args = parser.parse_args()

    return ParsedIndexingArguments(
        collection_name=args.collection_name,
        data_source_fqn=args.data_source_fqn,
        data_ingestion_run_name=args.data_ingestion_run_name,
        data_ingestion_mode=DataIngestionMode(args.data_ingestion_mode),
        raise_error_on_failture=args.raise_error_on_failture == "True",
        batch_size=int(args.batch_size),
    )