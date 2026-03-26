import polars as pl

from bank_to_actualbudget.file_io.base import WriteLFObject
from bank_to_actualbudget.log import get_logger
from bank_to_actualbudget.revolut.schemas import (
    ACCOUNT_TYPE_MAPPING,
    DESCRIPTION_MAPPING,
    INPUT_COLUMNS_MAPPINGS,
    PAYMENT_TYPE_MAPPING,
)

log = get_logger(__name__)


class Processor:
    def __init__(self, raw_lf: pl.LazyFrame):
        self.raw_lf = raw_lf
        self._process_lf: pl.LazyFrame = raw_lf
        self._output: list[WriteLFObject] = []

    def rename_columns(self) -> None:
        self._process_lf = self._process_lf.rename(INPUT_COLUMNS_MAPPINGS).select(
            list(INPUT_COLUMNS_MAPPINGS.values())
        )

    def normalize_cols(self) -> None:
        self._process_lf = self._process_lf.with_columns(
            payment_type=pl.col("payment_type").replace_strict(PAYMENT_TYPE_MAPPING),
            account_type=pl.col("account_type").replace_strict(ACCOUNT_TYPE_MAPPING),
            description=pl.col("description").replace(DESCRIPTION_MAPPING),
        )

    def format_dates(self) -> None:
        self._process_lf = self._process_lf.with_columns(
            pl.col("movement_date").str.to_datetime().dt.strftime("%Y-%m-%d")
        )

    def apply_fee(self) -> None:
        self._process_lf = self._process_lf.with_columns(
            (pl.col("amount") - pl.col("fee")).round(2).alias("amount")
        )

    def _savings(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.filter(
            (pl.col("account_type") == "revolut_savings")
            & (pl.col("payment_type") == "Interest")
        )

    def _revolut(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.filter(pl.col("account_type") == "revolut").with_columns(
            pl.when(pl.col("payment_type") == "Transfer")
            .then(pl.col("description"))
            .alias("payee")
        )

    def split_tables(self) -> None:
        self._output = [
            {
                "product": "revolut",
                "lf": self._revolut(self._process_lf),
            },
            {
                "product": "revolut_savings",
                "lf": self._savings(self._process_lf),
            },
        ]

    def _execute_step(self, step_name: str, func):
        """Helper to log the start/end of each step."""
        log.info(f"Step: {step_name}...")
        func()
        log.debug(f"Finished {step_name}")

    def run(self) -> list[WriteLFObject]:
        """Orchestrates the steps with automatic logging."""
        log.info(" [+] Starting process for revolut processor")

        try:
            self._execute_step("Renaming Columns", self.rename_columns)
            self._execute_step("normalize main column", self.normalize_cols)
            self._execute_step("format the datetime column", self.format_dates)
            self._execute_step("apply fees to ammount", self.apply_fee)
            self._execute_step("split the tables", self.split_tables)
            log.info(" [+] Process completed successfully.")
            return self._output
        except Exception as e:
            log.error(f" [!] Process failed: {str(e)}")
            raise
