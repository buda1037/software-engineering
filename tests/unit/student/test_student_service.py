"""Unit-Tests für find_by_id() von StudentService."""

from dataclasses import asdict
from datetime import date
from decimal import Decimal
from unittest.mock import create_autospec, patch

import pytest

from student.entity import Address, ExamResult, Gender, Student, StudyProgram
from student.repository.student_repository import StudentRepository
from student.service.exceptions import NotFoundError
from student.service.student_dto import StudentDTO
from student.service.student_service import StudentService


def test_find_by_id() -> None:
    # Arrange
    student_id = 1000
    student = Student(
        id=student_id,
        matriculation_number="123456",
        username="teststudent",
        first_name="Test",
        last_name="Student",
        gender=Gender.MALE,
        date_of_birth=date(2004, 5, 17),
        email="test.student@example.invalid",
        study_program=StudyProgram.WIRTSCHAFTSINFORMATIK,
        enrollment_date=date(2024, 10, 1),
        address=Address(
            street="Musterstraße",
            house_number="1a",
            postal_code="76133",
            city="Karlsruhe",
        ),
        exam_results=[
            ExamResult(
                module="Software Engineering",
                grade=Decimal("1.3"),
                ects=5,
                exam_date=date(2026, 7, 20),
            ),
        ],
    )

    repo_mock = create_autospec(StudentRepository, instance=True)
    repo_mock.find_by_id.return_value = student
    service = StudentService(repo=repo_mock)

    # Act
    with patch("student.service.student_service.Session") as session_factory:
        session_mock = session_factory.return_value.__enter__.return_value
        student_dto = service.find_by_id(student_id=student_id)

    # Assert
    session_factory.assert_called_once_with()
    repo_mock.find_by_id.assert_called_once_with(
        student_id=student_id,
        session=session_mock,
    )
    session_mock.commit.assert_called_once_with()

    assert isinstance(student_dto, StudentDTO)
    assert asdict(student_dto) == {
        "id": student_id,
        "matriculation_number": "123456",
        "username": "teststudent",
        "first_name": "Test",
        "last_name": "Student",
        "gender": Gender.MALE,
        "date_of_birth": date(2004, 5, 17),
        "email": "test.student@example.invalid",
        "study_program": StudyProgram.WIRTSCHAFTSINFORMATIK,
        "enrollment_date": date(2024, 10, 1),
        "address": {
            "street": "Musterstraße",
            "house_number": "1a",
            "postal_code": "76133",
            "city": "Karlsruhe",
        },
        "exam_results": [
            {
                "module": "Software Engineering",
                "grade": Decimal("1.3"),
                "ects": 5,
                "exam_date": date(2026, 7, 20),
            },
        ],
    }


def test_find_by_id_not_found() -> None:
    # Arrange
    student_id = 9999
    repo_mock = create_autospec(StudentRepository, instance=True)
    repo_mock.find_by_id.return_value = None
    service = StudentService(repo=repo_mock)

    # Act
    with patch("student.service.student_service.Session") as session_factory:
        session_mock = session_factory.return_value.__enter__.return_value

        with pytest.raises(NotFoundError) as err:
            service.find_by_id(student_id=student_id)

    # Assert
    session_factory.assert_called_once_with()
    repo_mock.find_by_id.assert_called_once_with(
        student_id=student_id,
        session=session_mock,
    )
    session_mock.commit.assert_not_called()
    assert err.value.student_id == student_id
