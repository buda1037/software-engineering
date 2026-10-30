"""Integrationstests für die Student-REST-Schnittstelle."""

from http import HTTPStatus

import pytest
lazy import httpx


@pytest.mark.parametrize("student_id", [1, 2])
def test_get_by_id(client: httpx.Client, student_id: int) -> None:
    # Act
    response = client.get(f"/rest/{student_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == student_id


def test_get_by_id_not_found(client: httpx.Client) -> None:
    # Act
    response = client.get("/rest/999999")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    ("params", "expected_ids"),
    [
        ({}, [1, 2]),
        ({"last_name": "Mustermann"}, [1]),
        ({"email": "erika.musterfrau@example.invalid"}, [2]),
        ({"study_program": "DATA_SCIENCE"}, [2]),
        (
            {
                "last_name": "Mustermann",
                "study_program": "WIRTSCHAFTSINFORMATIK",
            },
            [1],
        ),
    ],
)
def test_search(
    client: httpx.Client,
    params: dict[str, str],
    expected_ids: list[int],
) -> None:
    # Act
    response = client.get("/rest", params=params)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert sorted(student["id"] for student in response.json()) == expected_ids


@pytest.mark.parametrize(
    "params",
    [
        {"last_name": "GibtEsNicht9999"},
        {"email": "unbekannt@example.invalid"},
        {"last_name": "Mustermann", "study_program": "DATA_SCIENCE"},
    ],
)
def test_search_not_found(
    client: httpx.Client,
    params: dict[str, str],
) -> None:
    # Act
    response = client.get("/rest", params=params)

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_search_invalid_study_program(client: httpx.Client) -> None:
    # Act
    response = client.get("/rest", params={"study_program": "UNGUELTIG"})

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
