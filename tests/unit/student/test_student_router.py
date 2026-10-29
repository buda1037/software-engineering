"""Unit-Tests für den Student-Router."""

from datetime import date
from decimal import Decimal
from unittest.mock import create_autospec
lazy from collections.abc import Iterator
lazy from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from student.entity import StudyProgram
from student.fastapi_app import app
from student.router.dependencies import get_service
from student.service.adresse_dto import AddressDTO
from student.service.exam_result_dto import ExamResultDTO
from student.service.exceptions import NotFoundError
from student.service.student_dto import StudentDTO
from student.service.student_service import StudentService


@pytest.fixture
def service_mock() -> Iterator[Mock]:
    mock = create_autospec(StudentService, instance=True)
    previous_override = app.dependency_overrides.get(get_service)
    app.dependency_overrides[get_service] = lambda: mock

    try:
        yield mock
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_service, None)
        else:
            app.dependency_overrides[get_service] = previous_override


@pytest.fixture
def student_dto() -> StudentDTO:
    return StudentDTO(
        id=4242,
        matriculation_number="123456",
        username=None,
        first_name="Test",
        last_name="Student",
        gender=None,
        date_of_birth=date(2004, 5, 17),
        email="test.student@example.invalid",
        study_program=StudyProgram.WIRTSCHAFTSINFORMATIK,
        enrollment_date=date(2024, 10, 1),
        address=AddressDTO(
            street="Musterstraße",
            house_number="1a",
            postal_code="76133",
            city="Karlsruhe",
        ),
        exam_results=[
            ExamResultDTO(
                module="Software Engineering",
                grade=Decimal("1.3"),
                ects=5,
                exam_date=date(2026, 7, 20),
            ),
        ],
    )


def test_get_by_id(service_mock: Mock, student_dto: StudentDTO) -> None:
    # Arrange
    service_mock.find_by_id.return_value = student_dto

    # Act
    with TestClient(app) as client:
        response = client.get(f"/rest/{student_dto.id}")

    # Assert
    service_mock.find_by_id.assert_called_once_with(student_id=student_dto.id)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": student_dto.id,
        "matriculation_number": "123456",
        "username": None,
        "first_name": "Test",
        "last_name": "Student",
        "gender": None,
        "date_of_birth": "2004-05-17",
        "email": "test.student@example.invalid",
        "study_program": "WIRTSCHAFTSINFORMATIK",
        "enrollment_date": "2024-10-01",
        "address": {
            "street": "Musterstraße",
            "house_number": "1a",
            "postal_code": "76133",
            "city": "Karlsruhe",
        },
        "exam_results": [
            {
                "module": "Software Engineering",
                "grade": "1.3",
                "ects": 5,
                "exam_date": "2026-07-20",
            },
        ],
    }


def test_get_by_id_not_found(service_mock: Mock) -> None:
    # Arrange
    student_id = 9999
    service_mock.find_by_id.side_effect = NotFoundError(student_id=student_id)

    # Act
    with TestClient(app) as client:
        response = client.get(f"/rest/{student_id}")

    # Assert
    service_mock.find_by_id.assert_called_once_with(student_id=student_id)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


def test_get_by_id_invalid_id(service_mock: Mock) -> None:
    # Act
    with TestClient(app) as client:
        response = client.get("/rest/ungueltig")

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    service_mock.find_by_id.assert_not_called()


def test_search_invalid_study_program(service_mock: Mock) -> None:
    # Act
    with TestClient(app) as client:
        response = client.get(
            "/rest",
            params={"study_program": "UNGUELTIG"},
        )

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    service_mock.find.assert_not_called()
