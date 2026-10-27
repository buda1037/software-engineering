"""Enum for the study program of a student."""

from enum import StrEnum

__all__ = ["StudyProgram"]


class StudyProgram(StrEnum):
    """Study program of a student."""

    WIRTSCHAFTSINFORMATIK = "WIRTSCHAFTSINFORMATIK"
    INTERNATIONALES_IT_BUSINESS = "INTERNATIONALES_IT_BUSINESS"
    DATA_SCIENCE = "DATA_SCIENCE"
