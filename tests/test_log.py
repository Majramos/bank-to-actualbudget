import logging
import sys

import pytest

from bank_to_actualbudget.log import get_logger


@pytest.fixture(autouse=True)
def clean_loggers():
    """Ensure a clean slate for every test."""
    # This clears the internal registry of loggers
    logging.Logger.manager.loggerDict.clear()
    yield


def test_get_logger_initialization():
    """Verify logger is created with correct level and a StreamHandler."""
    name = "test_init"
    logger = get_logger(name)

    # Check level (INFO is 20)
    assert logger.level == logging.INFO
    # Check handler exists
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    # Check it's directed to stdout
    assert logger.handlers[0].stream == sys.stdout


def test_get_logger_formatter_config():
    """Check if the formatter string is applied correctly."""
    name = "test_formatter"
    logger = get_logger(name)

    # Ensure handler exists before accessing index 0
    assert len(logger.handlers) > 0
    handler = logger.handlers[0]
    formatter = handler.formatter

    assert "%(levelname)-7s" in formatter._fmt
    assert "%Y-%m-%d %H:%M:%S" == formatter.datefmt


def test_get_logger_prevents_duplicate_handlers():
    """Ensure that calling get_logger twice doesn't stack handlers."""
    name = "test_duplicate"

    # First call initializes
    logger_first = get_logger(name)
    # Second call should return the same logger without adding more handlers
    logger_second = get_logger(name)

    assert logger_first is logger_second
    assert len(logger_second.handlers) == 1


def test_get_logger_skips_config_if_handlers_exist(mocker):
    """
    Verify that if a logger already has handlers,
    the configuration logic is skipped entirely.
    """
    name = "test_already_has_handlers"
    logger = logging.getLogger(name)

    # Manually add a dummy handler so hasHandlers() returns True
    logger.addHandler(logging.NullHandler())

    # Spy on setLevel
    spy_set_level = mocker.spy(logger, "setLevel")

    result = get_logger(name)

    assert result is logger
    # Should only have the 1 NullHandler we added, not the StreamHandler
    assert len(result.handlers) == 1
    assert not spy_set_level.called
