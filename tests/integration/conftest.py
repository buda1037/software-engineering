"""Fixtures für Integrationstests gegen den laufenden Student-Server."""

from http import HTTPStatus
from os import environ
from pathlib import Path
from ssl import create_default_context
from typing import Any
lazy from collections.abc import Iterator

import psycopg
import pytest
from psycopg import sql
lazy import httpx


def _create_client(username: str | None = None) -> httpx.Client:
    """Erzeugt einen HTTP-Client, optional mit dem Token des Benutzers."""
    certificate = (
        Path(__file__).resolve().parents[2]
        / "src/student/config/resources/tls/certificate.crt"
    )
    http_client = httpx.Client(
        base_url="https://localhost:8000",
        verify=create_default_context(cafile=str(certificate)),
        timeout=10.0,
    )
    if username is not None:
        response = http_client.post(
            "/auth/token",
            json={"username": username, "password": "p"},
        )
        assert response.status_code == HTTPStatus.OK, response.text
        http_client.headers["Authorization"] = f"Bearer {response.json()['token']}"
    return http_client


@pytest.fixture(scope="session")
def client() -> Iterator[httpx.Client]:
    """Stellt einen HTTP-Client mit dem Token des Benutzers admin bereit."""
    http_client = _create_client(username="admin")
    yield http_client
    http_client.close()


@pytest.fixture(scope="session")
def student_client() -> Iterator[httpx.Client]:
    """Stellt einen HTTP-Client mit dem Token von mamu1011 (Student 1) bereit."""
    http_client = _create_client(username="mamu1011")
    yield http_client
    http_client.close()


@pytest.fixture(scope="session")
def client_without_token() -> Iterator[httpx.Client]:
    """Stellt einen HTTP-Client ohne Token bereit."""
    http_client = _create_client()
    yield http_client
    http_client.close()


@pytest.fixture(autouse=True)
def populate_database() -> None:
    """Legt das lokale Student-Schema vor jedem Test mit den Beispieldaten neu an."""
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


@pytest.fixture
def new_student() -> dict[str, Any]:
    """Stellt die Daten eines Studenten bereit, der nicht in den Beispieldaten ist."""
    return {
        "matriculation_number": "777777",
        "username": "jado1012",
        "first_name": "Jane",
        "last_name": "Doe",
        "gender": "FEMALE",
        "date_of_birth": "2005-03-14",
        "email": "jane.doe@example.com",
        "study_program": "DATA_SCIENCE",
        "enrollment_date": "2025-10-01",
        "address": {
            "street": "Moltkestraße",
            "house_number": "30",
            "postal_code": "76133",
            "city": "Karlsruhe",
        },
        "exam_results": [
            {
                "module": "Statistik",
                "grade": 1.7,
                "ects": 6,
                "exam_date": "2026-02-10",
            },
        ],
    }
