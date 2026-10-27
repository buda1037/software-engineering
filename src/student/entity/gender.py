"""Enum for the gender of a student."""

from enum import StrEnum

__all__ = ["Gender"]


class Gender(StrEnum):
    """Gender of a student."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    DIVERSE = "DIVERSE"
