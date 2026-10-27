"""Base class for the entity classes."""

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

__all__ = ["Base"]


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class that maps the entity classes as dataclasses."""
