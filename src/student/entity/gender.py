"""Enum für das Geschlecht eines Studenten."""

from enum import StrEnum

import strawberry

__all__ = ["Gender"]


@strawberry.enum
class Gender(StrEnum):
    """Geschlecht eines Studenten."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    DIVERSE = "DIVERSE"
