"""Geschäftslogik zum Schreiben von Studentendaten."""

from loguru import logger

from student.repository import Session, StudentRepository

__all__ = ["StudentWriteService"]


class StudentWriteService:
    """Service-Klasse mit Geschäftslogik zum Schreiben von Studentendaten."""

    def __init__(self, repo: StudentRepository) -> None:
        """Konstruktor mit abhängigem StudentRepository."""
        self.repo: StudentRepository = repo

    def delete_by_id(self, student_id: int) -> None:
        """Einen Studenten anhand seiner ID löschen.

        :param student_id: ID des zu löschenden Studenten
        """
        logger.debug("student_id={}", student_id)
        with Session() as session:
            self.repo.delete_by_id(student_id=student_id, session=session)
            session.commit()
