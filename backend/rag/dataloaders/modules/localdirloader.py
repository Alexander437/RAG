import os
import shutil
from typing import Dict, Iterator, List

from backend.logger import logger
from backend.rag.dataloaders.loader import BaseDataLoader
from backend.rag.schemas import DataIngestionMode, DataPoint, DataSource, LoadedDataPoint


class LocalDirLoader(BaseDataLoader):
    """
    Загрузка данных из локальной директории
    """
    def load_filtered_data(self,
                           data_source: DataSource,
                           dest_dir: str,
                           previous_snapshot: Dict[str, str],
                           batch_size: int,
                           data_ingestion_mode: DataIngestionMode) -> Iterator[List[LoadedDataPoint]]:
        """
        Загружает данные из локальной директории, определенной в URI
        """
        # Data source URI is the path of the local directory.
        source_dir = data_source.uri

        # Check if the source_dir is a relative path or an absolute path.
        if not os.path.isabs(source_dir):
            source_dir = os.path.join(os.getcwd(), source_dir)

        # Check if the source directory exists.
        if not os.path.exists(source_dir):
            raise Exception("Source directory does not exist")

        # If the source directory and destination directory are the same, do nothing.
        logger.info("source_dir: %s", source_dir)
        logger.info("dest_dir: %s", dest_dir)
        if source_dir == dest_dir:
            # Temrinate the function
            return

        # Copy the entire directory (including subdirectories) from source to destination.
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)

        loaded_data_points: List[LoadedDataPoint] = []
        for root, d_names, f_names in os.walk(dest_dir):
            for f in f_names:
                if f.startswith("."):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, dest_dir)
                file_ext = os.path.splitext(f)[1]
                data_point = DataPoint(
                    data_source_fqn=data_source.fqn,
                    data_point_uri=rel_path,
                    data_point_hash=str(os.path.getsize(full_path)),
                    local_filepath=full_path,
                    file_extension=file_ext,
                )

                # If the data ingestion mode is incremental, check if the data point already exists.
                if (
                    data_ingestion_mode == DataIngestionMode.INCREMENTAL
                    and previous_snapshot.get(data_point.data_point_fqn)
                    and previous_snapshot.get(data_point.data_point_fqn)
                    == data_point.data_point_hash
                ):
                    continue

                loaded_data_points.append(
                    LoadedDataPoint(
                        data_point_hash=data_point.data_point_hash,
                        data_point_uri=data_point.data_point_uri,
                        data_source_fqn=data_point.data_source_fqn,
                        local_filepath=full_path,
                        file_extension=file_ext,
                    )
                )
                if len(loaded_data_points) >= batch_size:
                    yield loaded_data_points
                    loaded_data_points.clear()
        yield loaded_data_points
