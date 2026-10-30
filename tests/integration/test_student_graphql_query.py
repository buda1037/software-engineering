"""Integrationstests für die GraphQL-Queries."""

from http import HTTPStatus
from operator import itemgetter
from typing import Any, Final

import pytest
lazy import httpx

STUDENT_FIELDS: Final = """
    id
    matriculationNumber
    username
    firstName
    lastName
    gender
    dateOfBirth
    email
    studyProgram
    enrollmentDate
    address { street houseNumber postalCode city }
    examResults { module grade ects examDate }
"""

STUDENT_QUERY: Final = f"query ($id: ID!) {{ student(id: $id) {{ {STUDENT_FIELDS} }} }}"

STUDENTS_QUERY: Final = f"""
query ($searchParameters: SearchParameters) {{
    students(searchParameters: $searchParameters) {{ {STUDENT_FIELDS} }}
}}
"""


def _query(
    client: httpx.Client,
    query: str,
    variables: dict[str, Any],
) -> dict[str, Any]:
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == HTTPStatus.OK
    return response.json()


def _to_camel_case(value: Any) -> Any:
    """Wandelt die Schlüssel einer REST-Antwort in die GraphQL-Schreibweise um."""
    if isinstance(value, dict):
        return {
            key.split("_")[0]
            + "".join(word.capitalize() for word in key.split("_")[1:]): (
                _to_camel_case(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_to_camel_case(item) for item in value]
    return value


@pytest.mark.parametrize("student_id", [1, 2])
def test_student(client: httpx.Client, student_id: int) -> None:
    # Arrange
    rest_student = client.get(f"/rest/{student_id}").json()

    # Act
    body = _query(client, STUDENT_QUERY, {"id": student_id})

    # Assert
    assert "errors" not in body
    assert body["data"]["student"] == _to_camel_case(rest_student)


def test_student_not_found(client: httpx.Client) -> None:
    # Act
    body = _query(client, STUDENT_QUERY, {"id": 999999})

    # Assert
    assert "errors" not in body
    assert body["data"]["student"] is None


@pytest.mark.parametrize(
    ("rest_params", "search_parameters"),
    [
        ({}, None),
        ({"last_name": "muster"}, {"lastName": "muster"}),
        (
            {"email": "erika.musterfrau@example.com"},
            {"email": "erika.musterfrau@example.com"},
        ),
        ({"study_program": "DATA_SCIENCE"}, {"studyProgram": "DATA_SCIENCE"}),
    ],
)
def test_students(
    client: httpx.Client,
    rest_params: dict[str, str],
    search_parameters: dict[str, str] | None,
) -> None:
    # Arrange
    rest_students = client.get("/rest", params=rest_params).json()

    # Act
    body = _query(client, STUDENTS_QUERY, {"searchParameters": search_parameters})

    # Assert
    assert "errors" not in body
    assert sorted(body["data"]["students"], key=itemgetter("id")) == sorted(
        _to_camel_case(rest_students),
        key=itemgetter("id"),
    )


def test_students_not_found(client: httpx.Client) -> None:
    # Act
    body = _query(
        client, STUDENTS_QUERY, {"searchParameters": {"lastName": "Unbekannt"}}
    )

    # Assert
    assert "errors" not in body
    assert body["data"]["students"] == []


@pytest.mark.parametrize(
    ("query", "variables"),
    [(STUDENT_QUERY, {"id": 1}), (STUDENTS_QUERY, {})],
)
def test_without_token(
    client_without_token: httpx.Client,
    query: str,
    variables: dict[str, Any],
) -> None:
    # Act
    body = _query(client_without_token, query, variables)

    # Assert
    assert body["errors"][0]["message"] == "Unauthorized"


def test_own_student_as_student(student_client: httpx.Client) -> None:
    # Act
    body = _query(student_client, STUDENT_QUERY, {"id": 1})

    # Assert
    assert "errors" not in body
    assert body["data"]["student"]["username"] == "mamu1011"


@pytest.mark.parametrize(
    ("query", "variables"),
    [(STUDENT_QUERY, {"id": 2}), (STUDENT_QUERY, {"id": 999999}), (STUDENTS_QUERY, {})],
)
def test_forbidden_as_student(
    student_client: httpx.Client,
    query: str,
    variables: dict[str, Any],
) -> None:
    # Act
    body = _query(student_client, query, variables)

    # Assert
    assert body["errors"][0]["message"] == "Forbidden"
