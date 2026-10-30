"""Enum für Rollen."""

from enum import StrEnum

__all__ = ["Role"]


class Role(StrEnum):
    """Enum für die Rollen des Clients in Keycloak."""

    ADMIN = "admin"
    """Rolle für die Administration."""

    STUDENT = "student"
    """Rolle für Studenten mit Zugriff auf die eigenen Daten."""
