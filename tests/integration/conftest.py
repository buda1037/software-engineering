"""Fixtures für Integrationstests gegen den laufenden Student-Server."""

from os import environ
from pathlib import Path
from ssl import create_default_context
lazy from collections.abc import Iterator

import psycopg
import pytest
from psycopg import sql
lazy import httpx


@pytest.fixture(scope="session")
def client() -> Iterator[httpx.Client]:
    """Stellt einen HTTP-Client mit dem lokalen Serverzertifikat bereit."""
    certificate = (
        Path(__file__).resolve().parents[2]
        / "src/student/config/resources/tls/certificate.crt"
    )
    tls_context = create_default_context(cafile=str(certificate))

    with httpx.Client(
        base_url="https://localhost:8000",
        verify=tls_context,
        timeout=10.0,
    ) as http_client:
        yield http_client


@pytest.fixture(scope="session", autouse=True)
def populate_database() -> None:
    """Legt das lokale Student-Schema mit den Beispieldaten neu an."""
    project_root = Path(__file__).resolve().parents[2]
    create_sql = project_root / "src/student/config/resources/postgresql/create.sql"
    csv_directory = project_root / "extras/compose/postgres/init/student/csv"

    with (
        psycopg.connect(
            host="localhost",
            dbname="student",
            user="student",
            password=environ["STUDENT_TEST_DB_PASSWORD"],
        ) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute("DROP SCHEMA IF EXISTS student CASCADE")
        cursor.execute("CREATE SCHEMA AUTHORIZATION student")
        cursor.execute("SET search_path TO student")
        cursor.execute(create_sql.read_bytes(), prepare=False)

        for table in ("student", "address", "exam_result"):
            copy_sql = sql.SQL(
                "COPY {} FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';')"
            ).format(sql.Identifier(table))

            with cursor.copy(copy_sql) as copy:
                copy.write(
                    (csv_directory / f"{table}.csv").read_text(
                        encoding="utf-8",
                    ),
                )
