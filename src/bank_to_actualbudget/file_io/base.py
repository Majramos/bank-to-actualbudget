from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Generic, TypeVar

TFrame = TypeVar("TFrame")


class FileIO(ABC, Generic[TFrame]):
    @abstractmethod
    def read(self, path: Path) -> TFrame:
        pass

    @abstractmethod
    def write(self, lf: TFrame) -> None:
        pass

    def get_timestamped_path(self, path: Path, dformat: str = "%Y%m%d%H%M%S") -> Path:
        ts = datetime.now().strftime(dformat)
        file_name = path.stem
        return path.with_stem(f"{file_name}_{ts}")
