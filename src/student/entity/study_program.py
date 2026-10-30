"""Enum für den Studiengang eines Studenten."""

from enum import StrEnum

import strawberry

__all__ = ["StudyProgram"]


@strawberry.enum
class StudyProgram(StrEnum):
    """Studiengang eines Studenten."""

    WIRTSCHAFTSINFORMATIK = "WIRTSCHAFTSINFORMATIK"
    INTERNATIONALES_IT_BUSINESS = "INTERNATIONALES_IT_BUSINESS"
    DATA_SCIENCE = "DATA_SCIENCE"
