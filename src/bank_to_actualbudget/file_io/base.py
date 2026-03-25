from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Generic, TypeVar

import polars as pl

T = TypeVar("T")


class FileIO(ABC, Generic[T]):
    @abstractmethod
    def read(self, path: Path) -> T:
        pass

    @abstractmethod
    def write(self, lf: pl.LazyFrame) -> None:
        pass

    def get_timestamped_path(self, path: Path, dformat: str = "%Y%m%d%H%M%S") -> Path:
        ts = datetime.now().strftime(dformat)
        file_name = path.stem
        return path.with_stem(f"{file_name}_{ts}")

    def validate_path(self, path: Path, extension: str = ".csv") -> None:
        """Centralized validation for file existence and type."""
        if not path.exists():
            raise FileNotFoundError(f"The file '{path}' does not exist.")

        if path.suffix.lower() != extension.lower():
            raise ValueError(f"File '{path}' is not a {extension} file.")
