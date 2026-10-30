"""Unit-Tests für die FastAPI-Anwendung."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from student.fastapi_app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_get_hello(client: TestClient) -> None:
    response = client.get("/hello")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World"}
