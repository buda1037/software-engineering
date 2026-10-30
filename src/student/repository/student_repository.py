"""Repository für persistente Studentendaten."""

from typing import Final
lazy from collections.abc import Sequence

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from student.entity import Student
lazy from student.repository.student_suchparameter import StudentSuchparameter

__all__ = ["StudentRepository"]


class StudentRepository:
    """Repository-Klasse für die Entity-Klasse Student."""

    def create(self, student: Student, session: Session) -> Student:
        """Einen neuen Studenten mit Adresse und Prüfungsergebnissen speichern.

        :param student: Der neue Student ohne ID
        :param session: Session für SQLAlchemy
        :return: Der neue Student mit generierter ID
        :rtype: Student
        """
        logger.debug("{}", student)
        session.add(student)
        session.flush(objects=[student])
        logger.debug("student_id={}", student.id)
        return student

    def exists_email(self, email: str, session: Session) -> bool:
        """Prüfen, ob die Emailadresse bereits verwendet wird.

        :param email: Die zu prüfende Emailadresse
        :param session: Session für SQLAlchemy
        :return: True, falls ein Student die Emailadresse hat
        :rtype: bool
        """
        statement: Final = select(Student.id).where(Student.email == email)
        return session.scalar(statement) is not None

    def exists_matriculation_number(
        self,
        matriculation_number: str,
        session: Session,
    ) -> bool:
        """Prüfen, ob die Matrikelnummer bereits verwendet wird.

        :param matriculation_number: Die zu prüfende Matrikelnummer
        :param session: Session für SQLAlchemy
        :return: True, falls ein Student die Matrikelnummer hat
        :rtype: bool
        """
        statement: Final = select(Student.id).where(
            Student.matriculation_number == matriculation_number,
        )
        return session.scalar(statement) is not None

    def exists_username(self, username: str, session: Session) -> bool:
        """Prüfen, ob der Benutzername bereits verwendet wird.

        :param username: Der zu prüfende Benutzername
        :param session: Session für SQLAlchemy
        :return: True, falls ein Student den Benutzernamen hat
        :rtype: bool
        """
        statement: Final = select(Student.id).where(Student.username == username)
        return session.scalar(statement) is not None

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

    def find(
        self,
        suchparameter: StudentSuchparameter,
        session: Session,
    ) -> Sequence[Student]:
        """Suche mit Suchparameter.

        :param suchparameter: Suchparameter für die Studentensuche
        :param session: Session für SQLAlchemy
        :return: Die gefundenen Studenten oder eine leere Liste
        :rtype: Sequence[Student]
        """
        logger.debug("{}", suchparameter)

        statement = select(Student).options(
            joinedload(Student.address),
            joinedload(Student.exam_results),
        )

        if suchparameter.last_name is not None:
            statement = statement.where(
                Student.last_name.icontains(
                    suchparameter.last_name,
                    autoescape=True,
                ),
            )

        if suchparameter.email is not None:
            statement = statement.where(Student.email == suchparameter.email)

        if suchparameter.study_program is not None:
            statement = statement.where(
                Student.study_program == suchparameter.study_program,
            )

        studenten: Final = session.scalars(statement).unique().all()
        logger.debug("{}", studenten)
        return studenten

    def delete_by_id(self, student_id: int, session: Session) -> None:
        """Lösche die Daten zu einem Studenten.

        :param student_id: Die ID des zu löschenden Studenten
        :param session: Session für SQLAlchemy
        """
        logger.debug("student_id={}", student_id)

        if (
            student := self.find_by_id(
                student_id=student_id,
                session=session,
            )
        ) is None:
            return

        session.delete(student)
        logger.debug("ok")
