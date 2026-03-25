from datetime import datetime
from pathlib import Path

import polars as pl
import pytest

from bank_to_actualbudget.file_io.base import FileIO, WriteLFObject


class ConcreteFileIO(FileIO[pl.DataFrame]):
    def read(self, path: Path) -> pl.DataFrame:
        return pl.DataFrame({"a": [1]})

    def write(self, lf_list: list[WriteLFObject]) -> None:
        pass


@pytest.fixture
def file_io():
    return ConcreteFileIO()


def test_get_timestamped_path(file_io, mocker):
    # Arrange
    path = Path("reports/sales.csv")
    product = "widget_a"
    fixed_now = datetime(2026, 3, 25, 14, 30, 0)

    # Use mocker to patch datetime in the module where FileIO is defined
    # Replace 'your_module' with the actual name of your python file
    mock_dt = mocker.patch("bank_to_actualbudget.file_io.base.datetime")
    mock_dt.now.return_value = fixed_now

    # Act
    result = file_io.get_timestamped_path(path=path, product=product)

    # Assert
    expected_name = "sales_widget_a_20260325143000.csv"
    assert result.name == expected_name
    assert result.parent == Path("reports")


def test_validate_path_exists_and_extension(file_io, tmp_path):
    # Setup: Create a real temporary file
    valid_file = tmp_path / "data.csv"
    valid_file.write_text("header\nvalue")

    # Should pass without exception
    file_io.validate_path(valid_file, extension=".csv")


def test_validate_path_raises_file_not_found(file_io):
    path = Path("ghost_file.csv")

    with pytest.raises(FileNotFoundError):
        file_io.validate_path(path)


def test_validate_path_raises_value_error_on_extension(file_io, tmp_path):
    wrong_ext_file = tmp_path / "data.txt"
    wrong_ext_file.touch()  # Creates the file

    with pytest.raises(ValueError, match="is not a .csv file"):
        file_io.validate_path(wrong_ext_file, extension=".csv")


def test_validate_path_case_insensitivity(file_io, tmp_path):
    # Test that .CSV matches .csv
    upper_file = tmp_path / "DATA.CSV"
    upper_file.touch()

    # Should not raise ValueError
    file_io.validate_path(upper_file, extension=".csv")
