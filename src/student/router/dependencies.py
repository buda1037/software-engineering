"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from student.repository.student_repository import StudentRepository
from student.service.student_service import StudentService


def get_repository() -> StudentRepository:
    """Factory-Funktion für StudentRepository.

    :return: Das Repository
    :rtype: StudentRepository
    """
    return StudentRepository()


def get_service(
    repo: Annotated[StudentRepository, Depends(get_repository)],
) -> StudentService:
    """Factory-Funktion für StudentService."""
    return StudentService(repo=repo)
