"""Integrationstests für die GraphQL-Mutation create."""

from http import HTTPStatus
from typing import Any, Final

import pytest
lazy import httpx

CREATE_MUTATION: Final = """
mutation ($student: StudentInput!) {
    create(student: $student) { id }
}
"""


@pytest.fixture
def student_input() -> dict[str, Any]:
    """Stellt die Daten eines neuen Studenten für GraphQL bereit."""
    return {
        "matriculationNumber": "777777",
        "username": "jado1012",
        "firstName": "Jane",
        "lastName": "Doe",
        "gender": "FEMALE",
        "dateOfBirth": "2005-03-14",
        "email": "jane.doe@example.com",
        "studyProgram": "DATA_SCIENCE",
        "enrollmentDate": "2025-10-01",
        "address": {
            "street": "Moltkestraße",
            "houseNumber": "30",
            "postalCode": "76133",
            "city": "Karlsruhe",
        },
        "examResults": [
            {
                "module": "Statistik",
                "grade": "1.7",
                "ects": 6,
                "examDate": "2026-02-10",
            },
        ],
    }


def _create(client: httpx.Client, student_input: dict[str, Any]) -> dict[str, Any]:
    response = client.post(
        "/graphql",
        json={"query": CREATE_MUTATION, "variables": {"student": student_input}},
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()


def test_create(client: httpx.Client, student_input: dict[str, Any]) -> None:
    # Act
    body = _create(client, student_input)

    # Assert
    assert "errors" not in body
    student_id = body["data"]["create"]["id"]
    student = client.get(f"/rest/{student_id}").json()
    assert student["matriculation_number"] == "777777"
    assert student["address"]["street"] == "Moltkestraße"
    assert student["exam_results"][0]["module"] == "Statistik"


def test_create_without_optional_values(
    client: httpx.Client,
    student_input: dict[str, Any],
) -> None:
    # Arrange
    del student_input["username"], student_input["gender"]
    del student_input["examResults"]

    # Act
    body = _create(client, student_input)

    # Assert
    assert "errors" not in body
    assert body["data"]["create"]["id"] > 0


@pytest.mark.parametrize(
    ("field", "value", "error_field"),
    [
        ("matriculationNumber", "12345", "matriculation_number"),
        ("firstName", "", "first_name"),
        ("email", "jane.doe", "email"),
        ("dateOfBirth", "2999-01-01", "date_of_birth"),
        (
            "address",
            {
                "street": "Moltkestraße",
                "houseNumber": "30",
                "postalCode": "7613",
                "city": "Karlsruhe",
            },
            "address.postal_code",
        ),
        (
            "examResults",
            [
                {
                    "module": "Statistik",
                    "grade": "6.0",
                    "ects": 6,
                    "examDate": "2026-02-10",
                }
            ],
            "exam_results.0.grade",
        ),
    ],
)
def test_create_invalid(
    client: httpx.Client,
    student_input: dict[str, Any],
    field: str,
    value: object,
    error_field: str,
) -> None:
    # Arrange
    student_input[field] = value

    # Act
    body = _create(client, student_input)

    # Assert
    assert body["data"] is None
    validation_errors = body["errors"][0]["extensions"]["validation_errors"]
    assert [error["field"] for error in validation_errors] == [error_field]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("email", "max.mustermann@example.com"),
        ("matriculationNumber", "123456"),
        ("username", "mamu1011"),
    ],
)
def test_create_value_exists(
    client: httpx.Client,
    student_input: dict[str, Any],
    field: str,
    value: str,
) -> None:
    # Arrange
    student_input[field] = value

    # Act
    body = _create(client, student_input)

    # Assert
    assert body["data"] is None
    assert value in body["errors"][0]["message"]


def test_create_without_token(
    client_without_token: httpx.Client,
    student_input: dict[str, Any],
) -> None:
    # Act
    body = _create(client_without_token, student_input)

    # Assert
    assert body["errors"][0]["message"] == "Unauthorized"


def test_create_as_student(
    student_client: httpx.Client,
    student_input: dict[str, Any],
) -> None:
    # Act
    body = _create(student_client, student_input)

    # Assert
    assert body["errors"][0]["message"] == "Forbidden"
