"""DB-URL erstellen."""

from typing import Final

from loguru import logger
from sqlalchemy.engine import URL

from student.config.config import app_config

__all__ = [
    "db_connect_args",
    "db_dialect",
    "db_log_statements",
    "db_url",
]


_db_toml: Final = app_config.get("db", {})

db_dialect: Final[str] = _db_toml.get("dialect", "postgresql")
"""DB-Dialekt für SQLAlchemy: 'postgresql'."""
logger.debug("db: db_dialect={}", db_dialect)

_drivername = "postgresql+psycopg"
_dbname: Final[str] = _db_toml.get("name", "student")
_host: Final[str] = _db_toml.get("host", "postgres")
_username: Final[str] = _db_toml.get("username", "student")
_password: Final[str] = _db_toml.get("password", "Change Me!")

db_log_statements: Final[bool] = bool(_db_toml.get("log-statements", False))
"""True, falls die SQL-Anweisungen protokolliert werden sollen."""

db_url: Final[URL] = URL.create(
    drivername=_drivername,
    username=_username,
    password=_password,
    host=_host,
    database=_dbname,
)
"""DB-URL für SQLAlchemy."""
logger.debug("db: db_url={}", db_url)

db_connect_args: Final[dict[str, int | None]] = {"prepare_threshold": None}
"""Zusätzliche Verbindungsparameter: keine Prepared Statements, damit die Tabellen
bei laufendem Server neu angelegt werden können, z.B. durch die Integrationstests."""
logger.debug("db: db_connect_args={}", db_connect_args)
