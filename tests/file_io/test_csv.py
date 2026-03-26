import polars as pl
import polars.testing as pl_test
import pytest

from bank_to_actualbudget.file_io.csv import CSVFileIO


@pytest.fixture
def csv_io():
    return CSVFileIO()


@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary CSV file for testing."""
    path = tmp_path / "input.csv"
    df = pl.DataFrame({"a": [1], "b": [2]})
    df.write_csv(path)
    return path


def test_read_success(mocker, csv_io, sample_csv):
    mock_log = mocker.patch("bank_to_actualbudget.file_io.csv.log")
    mock_validate = mocker.patch.object(CSVFileIO, "validate_path")

    # Act
    lf = csv_io.read(sample_csv)

    # Assert
    mock_validate.assert_called_once_with(sample_csv, extension=".csv")
    mock_log.info.assert_called_with(f"Reading file: {sample_csv}")
    assert isinstance(lf, pl.LazyFrame)
    assert csv_io._input_path == sample_csv


def test_write_logic(mocker, csv_io, sample_csv, tmp_path):
    # Setup state
    csv_io._input_path = sample_csv
    mock_log = mocker.patch("bank_to_actualbudget.file_io.csv.log")
    output_file = tmp_path / "output_test.csv"
    mocker.patch.object(CSVFileIO, "get_timestamped_path", return_value=output_file)

    # Create dummy LazyFrame data
    df_to_write = pl.DataFrame({"data": [100]})
    lf_obj = {"product": "savings", "lf": df_to_write.lazy()}

    # Act
    csv_io.write([lf_obj])

    # Assert
    assert output_file.exists()

    result_df = pl.read_csv(output_file)
    pl_test.assert_frame_equal(result_df, df_to_write)

    # Verify logging
    mock_log.info.assert_called_with(f"Writing file: {output_file}")


def test_write_missing_input_path(csv_io):
    # Act / Assert
    with pytest.raises(AttributeError):
        csv_io.write([{"product": "x", "lf": pl.LazyFrame()}])
