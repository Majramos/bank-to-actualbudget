from pathlib import Path

import polars as pl

from bank_to_actualbudget.file_io.base import FileIO, WriteLFObject
from bank_to_actualbudget.log import get_logger

log = get_logger(__name__)


class CSVFileIO(FileIO[pl.LazyFrame]):
    def __init__(self) -> None:
        self._input_path: Path

    def read(self, path: Path) -> pl.LazyFrame:
        self.validate_path(path, extension=".csv")
        self._input_path = path

        log.info(f"Reading file: {path}")
        return pl.scan_csv(path)

    def write(self, lf_list: list[WriteLFObject]) -> None:
        for obj in lf_list:
            output_path = self.get_timestamped_path(
                path=self._input_path, product=obj["product"]
            )
            df = obj["lf"].collect()
            log.info(f"Writing file: {output_path}")
            df.write_csv(output_path)
