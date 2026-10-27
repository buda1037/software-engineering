"""Enum for the gender of a student."""

from enum import StrEnum

import strawberry

__all__ = ["Gender"]


@strawberry.enum
class Gender(StrEnum):
    """Gender of a student."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    DIVERSE = "DIVERSE"
