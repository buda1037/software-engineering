"""Pydantic-Modell für ein Prüfungsergebnis eines Studenten."""

from typing import Annotated
lazy from datetime import date
lazy from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from student.entity import ExamResult

__all__ = ["ExamResultModel"]


class ExamResultModel(BaseModel):
    """Pydantic-Modell für ein Prüfungsergebnis eines Studenten."""

    module: Annotated[str, Field(min_length=1)]
    grade: Annotated[
        Decimal,
        Field(ge=Decimal("1.0"), le=Decimal("5.0"), max_digits=2, decimal_places=1),
    ]
    """Note von 1,0 bis 5,0."""
    ects: Annotated[int, Field(gt=0)]
    exam_date: date

    model_config = ConfigDict(extra="forbid", frozen=True)

    def to_exam_result(self) -> ExamResult:
        """Konvertierung in ein Entity-Objekt für SQLAlchemy.

        :return: ExamResult-Objekt für SQLAlchemy
        :rtype: ExamResult
        """
        return ExamResult(
            module=self.module,
            grade=self.grade,
            ects=self.ects,
            exam_date=self.exam_date,
        )
