"""Konfiguration aus der TOML-Datei einlesen."""

from importlib.resources import files
from pathlib import Path
from sys import stderr
from tomllib import load
from typing import Any, Final
lazy from importlib.resources.abc import Traversable

from loguru import logger

__all__ = ["app_config", "resources_path"]


resources_path: Final[str] = "student.config.resources"
_resources_traversable: Final[Traversable] = files(resources_path)
_config_file: Final[Traversable] = _resources_traversable / "app.toml"

with _config_file.open("rb") as reader:
    app_config: Final[dict[str, Any]] = load(reader)

_logger_toml: Final = app_config.get("logger", {})
_logger_debug: Final[bool] = bool(_logger_toml.get("debug-level", False))

LOG_FILE: Final = Path("log") / "app.log"
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html
# https://realpython.com/python-loguru
if _logger_debug:
    logger.add(LOG_FILE, rotation="1 MB")
else:
    logger.remove()  # remove default handler
    logger.add(stderr, level="INFO")
    logger.add(LOG_FILE, rotation="1 MB", level="INFO")

logger.info("Logging ist konfiguriert")
logger.debug("config: _config_file={}", _config_file)
logger.debug("config: app_config={}", app_config)
