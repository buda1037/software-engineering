"""Pydantic-Modell für die geänderten Daten eines Studenten."""

from typing import Annotated
lazy from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PastDate

from student.service.student_update import StudentUpdate
lazy from student.entity import Gender, StudyProgram

__all__ = ["StudentUpdateModel"]


class StudentUpdateModel(BaseModel):
    """Pydantic-Modell für die geänderten Daten eines Studenten.

    Adresse und Prüfungsergebnisse werden nicht geändert.
    """

    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    gender: Gender | None = None
    date_of_birth: PastDate
    email: EmailStr
    study_program: StudyProgram
    enrollment_date: date

    model_config = ConfigDict(extra="forbid", frozen=True)

    def to_student_update(self) -> StudentUpdate:
        """Konvertierung in die geänderten Daten für den Service.

        :return: Geänderte Daten des Studenten
        :rtype: StudentUpdate
        """
        return StudentUpdate(
            first_name=self.first_name,
            last_name=self.last_name,
            gender=self.gender,
            date_of_birth=self.date_of_birth,
            email=self.email,
            study_program=self.study_program,
            enrollment_date=self.enrollment_date,
        )
