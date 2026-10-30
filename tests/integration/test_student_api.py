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
