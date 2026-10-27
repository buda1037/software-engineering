"""Enum for the study program of a student."""

from enum import StrEnum

import strawberry

__all__ = ["StudyProgram"]


@strawberry.enum
class StudyProgram(StrEnum):
    """Study program of a student."""

    WIRTSCHAFTSINFORMATIK = "WIRTSCHAFTSINFORMATIK"
    INTERNATIONALES_IT_BUSINESS = "INTERNATIONALES_IT_BUSINESS"
    DATA_SCIENCE = "DATA_SCIENCE"
