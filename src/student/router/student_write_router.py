"""Router zum Schreiben von Studentendaten."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Response, status
from loguru import logger

from student.router.dependencies import get_write_service
lazy from student.service.student_write_service import StudentWriteService

__all__ = ["student_write_router"]


student_write_router: Final = APIRouter(tags=["Schreiben"])


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
