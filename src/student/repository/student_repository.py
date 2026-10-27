"""Repository für Studentendaten im Arbeitsspeicher."""

from datetime import date
from decimal import Decimal
from typing import Final

from student.entity import Address, ExamResult, Gender, Student, StudyProgram

__all__ = ["StudentRepository"]


_STUDENTS: Final[list[Student]] = [
    Student(
        id=1000,
        matriculation_number="123456",
        username="mamu1011",
        first_name="Max",
        last_name="Mustermann",
        gender=Gender.MALE,
        date_of_birth=date(2004, 5, 17),
        email="max.mustermann@example.invalid",
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
    ),
    Student(
        id=1001,
        matriculation_number="654321",
        username=None,
        first_name="Erika",
        last_name="Musterfrau",
        gender=Gender.FEMALE,
        date_of_birth=date(2003, 8, 12),
        email="erika.musterfrau@example.invalid",
        study_program=StudyProgram.DATA_SCIENCE,
        enrollment_date=date(2023, 10, 1),
        address=Address(
            street="Beispielstraße",
            house_number="2",
            postal_code="76135",
            city="Karlsruhe",
        ),
        exam_results=[],
    ),
]


class StudentRepository:
    """Repository-Klasse für die Entity-Klasse Student."""

    def find_by_id(self, student_id: int | None) -> Student | None:
        """Suche mit der Student-ID.

        :param student_id: ID des gesuchten Studenten
        :return: Der gefundene Student oder None
        :rtype: Student | None
        """
        if student_id is None:
            return None

        return next(
            (student for student in _STUDENTS if student.id == student_id),
            None,
        )
