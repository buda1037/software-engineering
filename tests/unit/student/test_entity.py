"""Unit tests for the entity classes."""

from datetime import date
from decimal import Decimal

from sqlalchemy import inspect

from student.entity import Address, ExamResult, Gender, Student, StudyProgram


def test_create_student_with_address_and_exam_results() -> None:
    address = Address(
        street="Musterstraße",
        house_number="1a",
        postal_code="76133",
        city="Karlsruhe",
    )
    exam_results = [
        ExamResult(
            module="Software Engineering",
            grade=Decimal("1.3"),
            ects=5,
            exam_date=date(2026, 7, 20),
        ),
        ExamResult(
            module="Datenbanken",
            grade=Decimal("2.0"),
            ects=5,
            exam_date=date(2026, 7, 24),
        ),
    ]

    student = Student(
        matriculation_number="123456",
        username="mamu1011",
        first_name="Max",
        last_name="Mustermann",
        gender=Gender.MALE,
        date_of_birth=date(2004, 5, 17),
        email="max.mustermann@example.com",
        study_program=StudyProgram.WIRTSCHAFTSINFORMATIK,
        enrollment_date=date(2024, 10, 1),
        address=address,
        exam_results=exam_results,
    )

    assert student.id is None
    assert student.address is address
    assert address.student is student
    assert student.exam_results == exam_results
    assert all(exam_result.student is student for exam_result in exam_results)


def test_tables_match_data_model() -> None:
    student = inspect(Student).local_table
    address = inspect(Address).local_table
    exam_result = inspect(ExamResult).local_table

    assert {c.name for c in student.columns if c.unique} == {
        "matriculation_number",
        "username",
        "email",
    }
    assert {c.name for c in student.columns if c.nullable} == {"gender", "username"}
    assert address.c.student_id.unique
    assert address.c.student_id.references(student.c.id)
    assert exam_result.c.student_id.references(student.c.id)
