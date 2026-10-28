"""DTO-Klasse für Prüfungsergebnisse ohne Decorators für SQLAlchemy."""

from dataclasses import dataclass
lazy from datetime import date
lazy from decimal import Decimal

import strawberry

lazy from student.entity import ExamResult


@dataclass(eq=False, slots=True, kw_only=True)
@strawberry.type(name="ExamResult")
class ExamResultDTO:
    """DTO-Klasse für die Daten eines Prüfungsergebnisses."""

    module: str
    grade: Decimal
    ects: int
    exam_date: date

    @classmethod
    def from_exam_result(cls, exam_result: ExamResult) -> ExamResultDTO:
        """Initialisierung von ExamResultDTO durch ein Entity-Objekt.

        :param exam_result: ExamResult-Objekt mit Decorators für SQLAlchemy
        :return: ExamResultDTO-Objekt mit Daten aus dem Entity-Objekt
        :rtype: ExamResultDTO
        """
        return cls(
            module=exam_result.module,
            grade=exam_result.grade,
            ects=exam_result.ects,
            exam_date=exam_result.exam_date,
        )
