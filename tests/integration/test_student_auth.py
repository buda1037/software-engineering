"""Integrationstests für Token und Zugriffsschutz."""

from http import HTTPStatus
from typing import Any

import pytest
lazy import httpx


def test_token(client_without_token: httpx.Client) -> None:
    # Act
    response = client_without_token.post(
        "/auth/token",
        json={"username": "admin", "password": "p"},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["token"]
    assert body["expires_in"] > 0
    assert body["roles"] == ["admin"]


@pytest.mark.parametrize(
    "body",
    [
        {"username": "admin", "password": "falsch"},
        {"username": "admin"},
        {"password": "p"},
        {},
    ],
)
def test_token_invalid(
    client_without_token: httpx.Client,
    body: dict[str, str],
) -> None:
    # Act
    response = client_without_token.post("/auth/token", json=body)

    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    ("method", "url"),
    [
        ("GET", "/rest/1"),
        ("GET", "/rest"),
        ("POST", "/rest"),
        ("PUT", "/rest/1"),
        ("DELETE", "/rest/1"),
    ],
)
def test_without_token(
    client_without_token: httpx.Client,
    method: str,
    url: str,
) -> None:
    # Act
    response = client_without_token.request(method, url)

    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_invalid_token(client_without_token: httpx.Client) -> None:
    # Act
    response = client_without_token.get(
        "/rest/1",
        headers={"Authorization": "Bearer ungueltig"},
    )

    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_own_data_as_student(student_client: httpx.Client) -> None:
    # Act
    response = student_client.get("/rest/1")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "mamu1011"


@pytest.mark.parametrize("url", ["/rest/2", "/rest/999999", "/rest"])
def test_get_forbidden_as_student(student_client: httpx.Client, url: str) -> None:
    # Act
    response = student_client.get(url)

    # Assert
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_write_forbidden_as_student(
    student_client: httpx.Client,
    new_student: dict[str, Any],
) -> None:
    # Act
    responses = [
        student_client.post("/rest", json=new_student),
        student_client.put("/rest/1", json=new_student),
        student_client.delete("/rest/2"),
    ]

    # Assert
    assert [response.status_code for response in responses] == [
        HTTPStatus.FORBIDDEN,
    ] * 3
