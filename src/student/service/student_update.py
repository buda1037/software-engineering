"""Geänderte Daten eines Studenten ohne Adresse und Prüfungsergebnisse."""

from dataclasses import dataclass
lazy from datetime import date

lazy from student.entity import Gender, StudyProgram

__all__ = ["StudentUpdate"]


@dataclass(frozen=True, slots=True, kw_only=True)
class StudentUpdate:
    """Geänderte Daten eines Studenten ohne Adresse und Prüfungsergebnisse."""

    first_name: str
    last_name: str
    gender: Gender | None
    date_of_birth: date
    email: str
    study_program: StudyProgram
    enrollment_date: date
