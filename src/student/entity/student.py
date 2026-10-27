"""Entity class for a student."""

lazy from datetime import date

from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from student.entity.base import Base
lazy from student.entity.address import Address
lazy from student.entity.exam_result import ExamResult
lazy from student.entity.gender import Gender
lazy from student.entity.study_program import StudyProgram

__all__ = ["Student"]


class Student(Base, kw_only=True, eq=False):
    """Entity class for a student."""

    __tablename__ = "student"

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
        nullable=False,
        default=None,
    )
    matriculation_number: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str | None] = mapped_column(unique=True, default=None)
    first_name: Mapped[str]
    last_name: Mapped[str]
    gender: Mapped[Gender | None] = mapped_column(default=None)
    date_of_birth: Mapped[date]
    email: Mapped[str] = mapped_column(unique=True)
    study_program: Mapped[StudyProgram]
    enrollment_date: Mapped[date]
    address: Mapped[Address] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
        repr=False,
    )
    exam_results: Mapped[list[ExamResult]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
        default_factory=list,
        repr=False,
    )
