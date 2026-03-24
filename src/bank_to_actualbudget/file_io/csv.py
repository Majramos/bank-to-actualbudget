from pathlib import Path

import polars as pl

from bank_to_actualbudget.file_io.base import FileIO


class CSVFileIO(FileIO[pl.LazyFrame]):
    def __init__(self) -> None:
        self._input_path: Path | None = None

    def read(self, path: Path) -> pl.LazyFrame:
        self._input_path = path
        self._output_path = path
        return pl.scan_csv(path)

    def write(self, lf: pl.LazyFrame) -> None:
        self.df = lf.collect()
        self.df.write_csv(self._output_path)
