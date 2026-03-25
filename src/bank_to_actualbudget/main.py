import argparse
from pathlib import Path

from bank_to_actualbudget.file_io.csv import CSVFileIO
from bank_to_actualbudget.log import get_logger
from bank_to_actualbudget.revolut.processor import Processor

log = get_logger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read and log the first 2 rows of a CSV file."
    )
    parser.add_argument("filename", help="The name of the CSV file to read")
    args = parser.parse_args()

    cwd = Path().resolve()
    file_path = cwd / args.filename
    log.info(f"file_name: {file_path}")

    file_io = CSVFileIO()
    file = file_io.read(cwd / args.filename)

    process = Processor(file)
    output = process.run()

    file_io.write(output)


if __name__ == "__main__":
    main()
