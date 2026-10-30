"""Benutzerdaten aus dem Token."""

from dataclasses import dataclass

lazy from student.security.role import Role

__all__ = ["User"]


@dataclass(frozen=True, eq=False, slots=True, kw_only=True)
class User:
    """Benutzerdaten aus dem Token."""

    username: str
    """Benutzername."""

    roles: list[Role]
    """Rollen als Liste von Enums."""
