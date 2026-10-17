"""Load the application configuration from TOML."""

from importlib.resources import files
from tomllib import load
from typing import Any, Final

__all__ = ["app_config", "resources_path"]

resources_path: Final[str] = "student.config.resources"
_config_file = files(resources_path).joinpath("app.toml")

with _config_file.open("rb") as reader:
    app_config: Final[dict[str, Any]] = load(reader)
