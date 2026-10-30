"""Pydantic-Modell für die Daten eines neuen Studenten."""

from typing import Annotated
lazy from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PastDate

from student.entity import Gender, Student, StudyProgram
lazy from student.router.address_model import AddressModel
lazy from student.router.exam_result_model import ExamResultModel

__all__ = ["StudentModel"]


class StudentModel(BaseModel):
    """Pydantic-Modell für die Daten eines neuen Studenten."""

    matriculation_number: Annotated[str, Field(pattern=r"^\d{6}$")]
    username: Annotated[str, Field(min_length=1)] | None = None
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    gender: Gender | None = None
    date_of_birth: PastDate
    email: EmailStr
    study_program: StudyProgram
    enrollment_date: date
    address: AddressModel
    exam_results: list[ExamResultModel] = []

    model_config = ConfigDict(extra="forbid", frozen=True)

    def to_student(self) -> Student:
        """Konvertierung in ein Entity-Objekt für SQLAlchemy.

        :return: Student-Objekt mit Adresse und Prüfungsergebnissen
        :rtype: Student
        """
        return Student(
            matriculation_number=self.matriculation_number,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            gender=self.gender,
            date_of_birth=self.date_of_birth,
            email=self.email,
            study_program=self.study_program,
            enrollment_date=self.enrollment_date,
            address=self.address.to_address(),
            exam_results=[
                exam_result.to_exam_result() for exam_result in self.exam_results
            ],
        )
