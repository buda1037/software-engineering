"""Integrationstests für PUT /rest/{id}."""

from http import HTTPStatus
from typing import Any

import pytest
lazy import httpx


@pytest.fixture
def student_update() -> dict[str, Any]:
    """Stellt die Daten von Student 1 mit neuem Nachnamen und neuer Email bereit."""
    return {
        "first_name": "Max",
        "last_name": "Neumann",
        "gender": "MALE",
        "date_of_birth": "2004-05-17",
        "email": "max.neumann@example.com",
        "study_program": "WIRTSCHAFTSINFORMATIK",
        "enrollment_date": "2024-10-01",
    }


def test_put(client: httpx.Client, student_update: dict[str, Any]) -> None:
    # Act
    response = client.put("/rest/1", json=student_update)

    # Assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    student = client.get("/rest/1").json()
    assert student["last_name"] == "Neumann"
    assert student["email"] == "max.neumann@example.com"
    assert student["matriculation_number"] == "123456"
    assert student["address"]["street"] == "Musterstraße"
    assert {exam["module"] for exam in student["exam_results"]} == {
        "Software Engineering",
        "Datenbanken",
    }


def test_put_same_email(
    client: httpx.Client,
    student_update: dict[str, Any],
) -> None:
    # Arrange
    student_update["email"] = "max.mustermann@example.com"

    # Act
    response = client.put("/rest/1", json=student_update)

    # Assert
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_put_not_found(
    client: httpx.Client,
    student_update: dict[str, Any],
) -> None:
    # Act
    response = client.put("/rest/999999", json=student_update)

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("last_name", ""),
        ("email", "max.neumann"),
        ("date_of_birth", "2999-01-01"),
        ("study_program", "INFORMATIK"),
        ("matriculation_number", "999999"),
    ],
)
def test_put_invalid(
    client: httpx.Client,
    student_update: dict[str, Any],
    field: str,
    value: str,
) -> None:
    # Arrange
    student_update[field] = value

    # Act
    response = client.put("/rest/1", json=student_update)

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


def test_put_email_exists(
    client: httpx.Client,
    student_update: dict[str, Any],
) -> None:
    # Arrange
    student_update["email"] = "erika.musterfrau@example.com"

    # Act
    response = client.put("/rest/1", json=student_update)

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert "erika.musterfrau@example.com" in response.json()["detail"]
