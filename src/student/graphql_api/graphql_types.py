"""Typen für GraphQL."""

lazy from datetime import date
lazy from decimal import Decimal

import strawberry

lazy from student.entity import Gender, StudyProgram

__all__ = [
    "AddressInput",
    "CreatePayload",
    "ExamResultInput",
    "StudentInput",
    "Suchparameter",
]


@strawberry.input
class Suchparameter:
    """Suchparameter für die Suche nach Studenten."""

    last_name: str | None = None
    """Teil des Nachnamens als Suchkriterium."""

    email: str | None = None
    """Exakte Emailadresse als Suchkriterium."""

    study_program: StudyProgram | None = None
    """Studiengang als Suchkriterium."""


@strawberry.input
class AddressInput:
    """Adresse eines neuen Studenten."""

    street: str
    """Straße."""

    house_number: str
    """Hausnummer."""

    postal_code: str
    """Postleitzahl mit 5 Ziffern."""

    city: str
    """Ort."""


@strawberry.input
class ExamResultInput:
    """Prüfungsergebnis eines neuen Studenten."""

    module: str
    """Modul."""

    grade: Decimal
    """Note zwischen 1.0 und 5.0."""

    ects: int
    """ECTS-Punkte."""

    exam_date: date
    """Prüfungsdatum."""


@strawberry.input
class StudentInput:
    """Daten für einen neuen Studenten, validiert wie der REST-Request-Body."""

    matriculation_number: str
    """Matrikelnummer mit 6 Ziffern."""

    first_name: str
    """Vorname."""

    last_name: str
    """Nachname."""

    date_of_birth: date
    """Geburtsdatum."""

    email: str
    """Emailadresse."""

    study_program: StudyProgram
    """Studiengang."""

    enrollment_date: date
    """Immatrikulationsdatum."""

    address: AddressInput
    """Adresse."""

    username: str | None = None
    """Optionaler Benutzername."""

    gender: Gender | None = None
    """Optionales Geschlecht."""

    exam_results: list[ExamResultInput] = strawberry.field(default_factory=list)
    """Prüfungsergebnisse."""


@strawberry.type
class CreatePayload:
    """Resultat, wenn ein neuer Student angelegt wurde."""

    id: int
    """ID des neuen Studenten."""
