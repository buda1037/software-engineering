"""Router zum Lesen von Studentendaten."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, HTTPException, Query, status

from student.router.dependencies import get_service
from student.router.student_find_model import (
    StudentFindModel,
    StudentResponseModel,
)
from student.security import Role, RolesRequired, User
from student.service.exceptions import ForbiddenError, NotFoundError
lazy from student.service.student_service import StudentService

__all__ = ["student_router"]


student_router: Final = APIRouter(tags=["Lesen"])


@student_router.get(
    path="/{student_id}",
    response_model=StudentResponseModel,
)
def get_by_id(
    student_id: int,
    user: Annotated[User, Depends(RolesRequired(Role.ADMIN, Role.STUDENT))],
    service: Annotated[StudentService, Depends(get_service)],
) -> StudentResponseModel:
    """Suche mit der Student-ID.

    :param student_id: ID des gesuchten Studenten
    :param user: Benutzer aus dem Token mit der Rolle admin oder student
    :param service: Injizierter Service für die Geschäftslogik
    :return: Antwortmodell mit dem gefundenen Studenten
    :rtype: StudentResponseModel
    :raises HTTPException: 404, falls kein Student gefunden wurde, oder 403,
        falls der Benutzer die Daten nicht lesen darf
    """
    try:
        student = service.find_by_id(student_id=student_id, user=user)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc

    return StudentResponseModel.from_dto(student)


@student_router.get(
    path="",
    response_model=list[StudentResponseModel],
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)
def get(
    find_model: Annotated[StudentFindModel, Query()],
    service: Annotated[StudentService, Depends(get_service)],
) -> list[StudentResponseModel]:
    """Suche mit Query-Parameter.

    :param find_model: Validierte Suchparameter als Pydantic-Modell
    :param service: Injizierter Service für Geschäftslogik
    :return: Liste der gefundenen Studenten
    :rtype: list[StudentResponseModel]
    :raises HTTPException: Falls keine Studenten gefunden wurden
    """
    try:
        studenten = service.find(
            suchparameter=find_model.to_suchparameter(),
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc

    return [StudentResponseModel.from_dto(student) for student in studenten]
