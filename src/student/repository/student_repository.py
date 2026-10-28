"""Repository für persistente Studentendaten."""

from typing import Final

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from student.entity import Student

__all__ = ["StudentRepository"]


class StudentRepository:
    """Repository-Klasse für die Entity-Klasse Student."""

    def find_by_id(self, student_id: int | None, session: Session) -> Student | None:
        """Suche mit der Student-ID.

        :param student_id: ID des gesuchten Studenten
        :param session: Session für SQLAlchemy
        :return: Der gefundene Student oder None
        :rtype: Student | None
        """
        logger.debug("student_id={}", student_id)

        if student_id is None:
            return None

        statement: Final = (
            select(Student)
            .options(
                joinedload(Student.address),
                joinedload(Student.exam_results),
            )
            .where(Student.id == student_id)
        )
        student: Final = session.scalars(statement).unique().one_or_none()

        logger.debug("{}", student)
        return student
