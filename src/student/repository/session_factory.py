"""Engine und die Factory für Sessions konfigurieren."""

from typing import Final

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from student.config.db import (
    db_connect_args,
    db_log_statements,
    db_url,
)

__all__ = ["Session", "engine"]


# https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
# Default Isolation Level "READ COMMITTED": Schreibsperren und keine Lesesperren
engine: Final = create_engine(
    db_url,
    connect_args=db_connect_args,
    poolclass=QueuePool,
    # Defaultwert: 5
    pool_size=10,
    echo=db_log_statements,
    # Parameterwerte nicht in SQL-Logs ausgeben.
    hide_parameters=True,
)
"""'Engine' für SQLAlchemy, um DB-Verbindungen und Sessions zu erstellen."""

logger.info("Engine fuer SQLAlchemy erzeugt")


# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
Session = sessionmaker(bind=engine, autoflush=False)
"""Factory für Sessions, um generierte SQL-Anweisungen in Transaktionen abzusetzen."""

logger.info("Session-Factory fuer SQLAlchemy erzeugt")
