"""DTO-Klasse für Studentendaten ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass
lazy from datetime import date

import strawberry

from student.service.adresse_dto import AddressDTO
from student.service.exam_result_dto import ExamResultDTO
lazy from student.entity import Gender, Student, StudyProgram

__all__ = ["StudentDTO"]


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type(name="Student")
class StudentDTO:
    """DTO-Klasse für gelesene oder gespeicherte Studentendaten."""

    id: int
    matriculation_number: str
    username: str | None
    first_name: str
    last_name: str
    gender: Gender | None
    date_of_birth: date
    email: str
    study_program: StudyProgram
    enrollment_date: date
    address: AddressDTO
    exam_results: list[ExamResultDTO]

    @classmethod
    def from_student(cls, student: Student) -> StudentDTO:
        """Initialisierung von StudentDTO durch ein Entity-Objekt von Student.

        :param student: Student-Objekt mit Decorators für SQLAlchemy
        :return: StudentDTO-Objekt mit Daten aus dem Student-Objekt
        :rtype: StudentDTO
        """
        return cls(
            id=student.id if student.id is not None else -1,
            matriculation_number=student.matriculation_number,
            username=student.username,
            first_name=student.first_name,
            last_name=student.last_name,
            gender=student.gender,
            date_of_birth=student.date_of_birth,
            email=student.email,
            study_program=student.study_program,
            enrollment_date=student.enrollment_date,
            address=AddressDTO.from_address(student.address),
            exam_results=[
                ExamResultDTO.from_exam_result(exam_result)
                for exam_result in student.exam_results
            ],
        )
