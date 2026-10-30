"""Geschäftslogik zum Lesen von Studentendaten."""

from typing import Final

from loguru import logger

from student.repository import Session, StudentRepository
from student.security.role import Role
from student.service.exceptions import ForbiddenError, NotFoundError
from student.service.student_dto import StudentDTO
lazy from student.repository.student_suchparameter import StudentSuchparameter
lazy from student.security.user import User

__all__ = ["StudentService"]


class StudentService:
    """Service-Klasse mit Geschäftslogik für Student."""

    def __init__(self, repo: StudentRepository) -> None:
        """Konstruktor mit abhängigem StudentRepository."""
        self.repo: StudentRepository = repo

    def find_by_id(self, student_id: int, user: User) -> StudentDTO:
        """Suche mit der Student-ID.

        Ein Admin darf alle Studenten lesen, ein Student nur die eigenen Daten.

        :param student_id: ID für die Suche
        :param user: Benutzer aus dem Token
        :return: Der gefundene Student als DTO
        :rtype: StudentDTO
        :raises NotFoundError: Falls ein Admin nach einer unbekannten ID sucht
        :raises ForbiddenError: Falls ein Student fremde Daten oder eine unbekannte
            ID sucht
        """
        logger.debug("student_id={}, user={}", student_id, user)
        user_is_admin: Final = Role.ADMIN in user.roles

        with Session() as session:
            if (
                student := self.repo.find_by_id(student_id=student_id, session=session)
            ) is None:
                if user_is_admin:
                    raise NotFoundError(student_id=student_id)
                raise ForbiddenError
            if not user_is_admin and student.username != user.username:
                raise ForbiddenError

            student_dto: Final = StudentDTO.from_student(student)
            session.commit()

        logger.debug("{}", student_dto)
        return student_dto

    def find(
        self,
        suchparameter: StudentSuchparameter,
    ) -> tuple[StudentDTO, ...]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter für die Studentensuche
        :return: Tupel der gefundenen Studenten als DTOs
        :rtype: tuple[StudentDTO, ...]
        :raises NotFoundError: Falls keine Studenten gefunden wurden
        """
        logger.debug("{}", suchparameter)

        with Session() as session:
            studenten: Final = self.repo.find(
                suchparameter=suchparameter,
                session=session,
            )
            if len(studenten) == 0:
                raise NotFoundError(suchparameter=suchparameter)

            studenten_dto: Final = tuple(
                StudentDTO.from_student(student) for student in studenten
            )
            session.commit()

        logger.debug("{}", studenten_dto)
        return studenten_dto
