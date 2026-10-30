"""Integrationstests für POST /rest."""

from http import HTTPStatus
from typing import Any

import pytest
lazy import httpx


def test_post(client: httpx.Client, new_student: dict[str, Any]) -> None:
    # Act
    response = client.post("/rest", json=new_student)

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    student = client.get(response.headers["Location"]).json()
    assert student["matriculation_number"] == "777777"
    assert student["address"]["street"] == "Moltkestraße"
    assert student["exam_results"][0]["module"] == "Statistik"


def test_post_without_optional_values(
    client: httpx.Client,
    new_student: dict[str, Any],
) -> None:
    # Arrange
    del new_student["username"], new_student["gender"], new_student["exam_results"]

    # Act
    response = client.post("/rest", json=new_student)

    # Assert
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("matriculation_number", "12345"),
        ("first_name", ""),
        ("email", "jane.doe"),
        ("date_of_birth", "2999-01-01"),
        ("study_program", "INFORMATIK"),
        ("address", {"street": "Moltkestraße"}),
        (
            "exam_results",
            [
                {
                    "module": "Statistik",
                    "grade": 6.0,
                    "ects": 6,
                    "exam_date": "2026-02-10",
                },
            ],
        ),
        (
            "exam_results",
            [
                {
                    "module": "Statistik",
                    "grade": 1.7,
                    "ects": 0,
                    "exam_date": "2026-02-10",
                },
            ],
        ),
        ("unknown", "value"),
    ],
)
def test_post_invalid(
    client: httpx.Client,
    new_student: dict[str, Any],
    field: str,
    value: object,
) -> None:
    # Arrange
    new_student[field] = value

    # Act
    response = client.post("/rest", json=new_student)

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("email", "max.mustermann@example.com"),
        ("matriculation_number", "123456"),
        ("username", "mamu1011"),
    ],
)
def test_post_value_exists(
    client: httpx.Client,
    new_student: dict[str, Any],
    field: str,
    value: str,
) -> None:
    # Arrange
    new_student[field] = value

    # Act
    response = client.post("/rest", json=new_student)

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert value in response.json()["detail"]
