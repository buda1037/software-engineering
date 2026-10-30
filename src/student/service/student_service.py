"""Geschäftslogik zum Lesen von Studentendaten."""

from typing import Final

from loguru import logger

from student.repository import Session, StudentRepository
from student.security.role import Role
from student.service.exceptions import ForbiddenError, NotFoundError
from student.service.student_dto import StudentDTO
lazy from student.repository.student_search_parameters import StudentSearchParameters
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
        search_parameters: StudentSearchParameters,
    ) -> tuple[StudentDTO, ...]:
        """Suche mit Suchparameter.

        :param search_parameters: Suchparameter für die Studentensuche
        :return: Tupel der gefundenen Studenten als DTOs
        :rtype: tuple[StudentDTO, ...]
        :raises NotFoundError: Falls keine Studenten gefunden wurden
        """
        logger.debug("{}", search_parameters)

        with Session() as session:
            students: Final = self.repo.find(
                search_parameters=search_parameters,
                session=session,
            )
            if len(students) == 0:
                raise NotFoundError(search_parameters=search_parameters)

            student_dtos: Final = tuple(
                StudentDTO.from_student(student) for student in students
            )
            session.commit()

        logger.debug("{}", student_dtos)
        return student_dtos
