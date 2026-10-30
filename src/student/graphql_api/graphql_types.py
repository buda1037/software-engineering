"""Typen für GraphQL."""

import strawberry

lazy from student.entity import StudyProgram

__all__ = ["Suchparameter"]


@strawberry.input
class Suchparameter:
    """Suchparameter für die Suche nach Studenten."""

    last_name: str | None = None
    """Teil des Nachnamens als Suchkriterium."""

    email: str | None = None
    """Exakte Emailadresse als Suchkriterium."""

    study_program: StudyProgram | None = None
    """Studiengang als Suchkriterium."""
