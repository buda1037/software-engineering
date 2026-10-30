"""Basisklasse für die Entity-Klassen."""

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

__all__ = ["Base"]


class Base(MappedAsDataclass, DeclarativeBase):
    """Basisklasse, die die Entity-Klassen als Dataclasses abbildet."""
