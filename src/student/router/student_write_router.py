"""Router zum Schreiben von Studentendaten."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from loguru import logger

from student.router.dependencies import get_write_service
from student.security import Role, RolesRequired
from student.service.exceptions import (
    EmailExistsError,
    MatriculationNumberExistsError,
    NotFoundError,
    UsernameExistsError,
)
lazy from student.router.student_model import StudentModel
lazy from student.router.student_update_model import StudentUpdateModel
lazy from student.service.student_write_service import StudentWriteService

__all__ = ["student_write_router"]


student_write_router: Final = APIRouter(
    tags=["Schreiben"],
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
)


@student_write_router.post("", status_code=status.HTTP_201_CREATED)
def post(
    student_model: StudentModel,
    request: Request,
    service: Annotated[StudentWriteService, Depends(get_write_service)],
) -> Response:
    """POST-Request, um einen neuen Studenten anzulegen.

    :param student_model: Validierte Daten des neuen Studenten
    :param request: Request, um die URL im Header Location zu bilden
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 201 und Header Location
    :rtype: Response
    :raises HTTPException: 422, falls Emailadresse, Matrikelnummer oder
        Benutzername bereits existieren
    """
    logger.debug("{}", student_model)
    try:
        student_dto: Final = service.create(student=student_model.to_student())
    except (
        EmailExistsError,
        MatriculationNumberExistsError,
        UsernameExistsError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"{request.url}/{student_dto.id}"},
    )


@student_write_router.put("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def put(
    student_id: int,
    student_update_model: StudentUpdateModel,
    service: Annotated[StudentWriteService, Depends(get_write_service)],
) -> Response:
    """PUT-Request, um die Daten eines Studenten zu ändern.

    Adresse und Prüfungsergebnisse bleiben unverändert.

    :param student_id: ID des zu ändernden Studenten
    :param student_update_model: Validierte geänderte Daten
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    :raises HTTPException: 404, falls kein Student zur ID existiert, oder 422,
        falls die neue Emailadresse bereits existiert
    """
    logger.debug("student_id={}, {}", student_id, student_update_model)
    try:
        service.update(
            student_id=student_id,
            update=student_update_model.to_student_update(),
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
    except EmailExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@student_write_router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(
    student_id: int,
    service: Annotated[StudentWriteService, Depends(get_write_service)],
) -> Response:
    """DELETE-Request, um einen Studenten anhand seiner ID zu löschen.

    :param student_id: ID des zu löschenden Studenten
    :param service: Injizierter Service für Geschäftslogik
    :return: Response mit Statuscode 204
    :rtype: Response
    """
    logger.debug("student_id={}", student_id)
    service.delete_by_id(student_id=student_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
