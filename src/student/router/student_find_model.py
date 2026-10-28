"""Pydantic-Modelle für das Lesen von Studentendaten."""

lazy from datetime import date
lazy from decimal import Decimal

from pydantic import BaseModel, ConfigDict

lazy from student.entity import Gender, StudyProgram
lazy from student.service.student_dto import StudentDTO

__all__ = ["StudentResponseModel"]


class AddressResponseModel(BaseModel):
    """Adresse als Teil eines Antwortmodells für Studenten."""

    street: str
    house_number: str
    postal_code: str
    city: str

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")


class ExamResultResponseModel(BaseModel):
    """Prüfungsergebnis als Teil eines Antwortmodells für Studenten."""

    module: str
    grade: Decimal
    ects: int
    exam_date: date

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")


class StudentResponseModel(BaseModel):
    """Pydantic-Modell für einen gefundenen Studenten."""

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
    address: AddressResponseModel
    exam_results: list[ExamResultResponseModel]

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")

    @classmethod
    def from_dto(cls, student: StudentDTO) -> StudentResponseModel:
        """Konvertiert ein StudentDTO in ein Pydantic-Modell für die Antwort.

        :param student: StudentDTO-Objekt aus dem Service
        :return: Pydantic-Modell mit den Daten des Studenten
        :rtype: StudentResponseModel
        """
        return cls.model_validate(student)
