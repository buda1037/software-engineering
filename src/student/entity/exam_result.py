"""Entity class for an exam result of a student."""

lazy from datetime import date
lazy from decimal import Decimal

from sqlalchemy import ForeignKey, Identity, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from student.entity.base import Base
lazy from student.entity.student import Student

__all__ = ["ExamResult"]


class ExamResult(Base, kw_only=True, eq=False):
    """Entity class for an exam result of a student."""

    __tablename__ = "exam_result"

    id: Mapped[int | None] = mapped_column(
        Identity(start=1000),
        primary_key=True,
        nullable=False,
        default=None,
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), init=False)
    module: Mapped[str]
    grade: Mapped[Decimal] = mapped_column(Numeric(2, 1))
    ects: Mapped[int]
    exam_date: Mapped[date]
    student: Mapped[Student] = relationship(
        back_populates="exam_results",
        init=False,
        repr=False,
    )
