"""Geschäftslogik zum Schreiben von Studentendaten."""

from typing import Final

from loguru import logger
lazy from sqlalchemy.orm import Session as SessionType

from student.repository import Session, StudentRepository
from student.service.exceptions import (
    EmailExistsError,
    MatriculationNumberExistsError,
    NotFoundError,
    UsernameExistsError,
)
from student.service.student_dto import StudentDTO
lazy from student.entity import Student
lazy from student.service.student_update import StudentUpdate

__all__ = ["StudentWriteService"]


class StudentWriteService:
    """Service-Klasse mit Geschäftslogik zum Schreiben von Studentendaten."""

    def __init__(self, repo: StudentRepository) -> None:
        """Konstruktor mit abhängigem StudentRepository."""
        self.repo: StudentRepository = repo

    def create(self, student: Student) -> StudentDTO:
        """Einen neuen Studenten anlegen.

        :param student: Der neue Student ohne ID
        :return: Der neu angelegte Student als DTO
        :rtype: StudentDTO
        :raises EmailExistsError: Falls die Emailadresse bereits existiert
        :raises MatriculationNumberExistsError: Falls die Matrikelnummer bereits
            existiert
        :raises UsernameExistsError: Falls der Benutzername bereits existiert
        """
        logger.debug("{}", student)

        with Session() as session:
            self._check_unique(student=student, session=session)
            self.repo.create(student=student, session=session)
            student_dto: Final = StudentDTO.from_student(student)
            session.commit()

        logger.debug("{}", student_dto)
        return student_dto

    def update(self, student_id: int, update: StudentUpdate) -> None:
        """Die Daten eines Studenten ohne Adresse und Prüfungsergebnisse ändern.

        :param student_id: ID des zu ändernden Studenten
        :param update: Die geänderten Daten
        :raises NotFoundError: Falls kein Student zur ID existiert
        :raises EmailExistsError: Falls die neue Emailadresse bereits existiert
        """
        logger.debug("student_id={}, {}", student_id, update)

        with Session() as session:
            if (
                student := self.repo.find_by_id(student_id=student_id, session=session)
            ) is None:
                raise NotFoundError(student_id=student_id)
            if update.email != student.email and self.repo.exists_email(
                email=update.email,
                session=session,
            ):
                raise EmailExistsError(email=update.email)

            student.first_name = update.first_name
            student.last_name = update.last_name
            student.gender = update.gender
            student.date_of_birth = update.date_of_birth
            student.email = update.email
            student.study_program = update.study_program
            student.enrollment_date = update.enrollment_date
            session.commit()

        logger.debug("student_id={} geaendert", student_id)

    def delete_by_id(self, student_id: int) -> None:
        """Einen Studenten anhand seiner ID löschen.

        :param student_id: ID des zu löschenden Studenten
        """
        logger.debug("student_id={}", student_id)
        with Session() as session:
            self.repo.delete_by_id(student_id=student_id, session=session)
            session.commit()

    def _check_unique(self, student: Student, session: SessionType) -> None:
        if self.repo.exists_email(email=student.email, session=session):
            raise EmailExistsError(email=student.email)
        if self.repo.exists_matriculation_number(
            matriculation_number=student.matriculation_number,
            session=session,
        ):
            raise MatriculationNumberExistsError(
                matriculation_number=student.matriculation_number,
            )
        if student.username is not None and self.repo.exists_username(
            username=student.username,
            session=session,
        ):
            raise UsernameExistsError(username=student.username)
