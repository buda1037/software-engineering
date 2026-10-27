"""Entity class for the address of a student."""

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from student.entity.base import Base
lazy from student.entity.student import Student

__all__ = ["Address"]


class Address(Base, kw_only=True, eq=False):
    """Entity class for the address of a student."""

    __tablename__ = "address"

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
        nullable=False,
        default=None,
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id"),
        unique=True,
        init=False,
    )
    street: Mapped[str]
    house_number: Mapped[str]
    postal_code: Mapped[str]
    city: Mapped[str]
    student: Mapped[Student] = relationship(
        back_populates="address",
        init=False,
        repr=False,
    )
