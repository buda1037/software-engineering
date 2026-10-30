"""Schema für GraphQL durch Strawberry."""

from typing import Annotated, Final

import strawberry
from fastapi import Request
from graphql import GraphQLError
from loguru import logger
from strawberry.fastapi import GraphQLRouter
lazy from strawberry.types import Info

from student.repository import StudentRepository
from student.repository.student_suchparameter import StudentSuchparameter
from student.security import AuthorizationError, Role, User
from student.security.dependencies import get_token_service
from student.service.exceptions import ForbiddenError, NotFoundError
from student.service.student_service import StudentService
lazy from student.graphql_api.graphql_types import Suchparameter
lazy from student.service.student_dto import StudentDTO

__all__ = ["graphql_router"]


_service: Final = StudentService(repo=StudentRepository())
_token_service: Final = get_token_service()


def _get_user(info: Info, *roles: Role) -> User:
    """Den Benutzer aus dem Token ermitteln und seine Rollen prüfen.

    :param info: Kontext mit dem Request
    :param roles: Rollen, von denen der Benutzer mindestens eine braucht
    :return: Der Benutzer aus dem Token
    :rtype: User
    :raises GraphQLError: Unauthorized bei fehlendem oder ungültigem Token,
        Forbidden bei fehlender Rolle
    """
    request: Final[Request] = info.context["request"]
    try:
        user: Final = _token_service.get_user_from_request(request)
    except AuthorizationError as err:
        raise GraphQLError("Unauthorized") from err
    if not any(role in user.roles for role in roles):
        raise GraphQLError("Forbidden")
    return user


@strawberry.type
class Query:
    """Queries, um Studentendaten zu lesen."""

    @strawberry.field
    def student(
        self,
        student_id: Annotated[strawberry.ID, strawberry.argument(name="id")],
        info: Info,
    ) -> StudentDTO | None:
        """Daten zu einem Studenten lesen.

        :param student_id: ID des gesuchten Studenten
        :param info: Kontext mit dem Request
        :return: Der gesuchte Student oder None
        :rtype: StudentDTO | None
        :raises GraphQLError: Falls der Benutzer die Daten nicht lesen darf
        """
        logger.debug("student_id={}", student_id)
        user: Final = _get_user(info, Role.ADMIN, Role.STUDENT)
        try:
            return _service.find_by_id(student_id=int(student_id), user=user)
        except NotFoundError:
            return None
        except ForbiddenError as err:
            raise GraphQLError("Forbidden") from err

    @strawberry.field
    def students(
        self,
        info: Info,
        suchparameter: Suchparameter | None = None,
    ) -> list[StudentDTO]:
        """Studenten anhand von Suchparametern suchen.

        :param info: Kontext mit dem Request
        :param suchparameter: Nachname, Emailadresse und Studiengang
        :return: Die gefundenen Studenten oder eine leere Liste
        :rtype: list[StudentDTO]
        :raises GraphQLError: Falls der Benutzer nicht admin ist
        """
        logger.debug("suchparameter={}", suchparameter)
        _get_user(info, Role.ADMIN)
        student_suchparameter: Final = (
            StudentSuchparameter()
            if suchparameter is None
            else StudentSuchparameter(
                last_name=suchparameter.last_name,
                email=suchparameter.email,
                study_program=suchparameter.study_program,
            )
        )
        try:
            return list(_service.find(suchparameter=student_suchparameter))
        except NotFoundError:
            return []


schema: Final = strawberry.Schema(query=Query)

type Context = dict[str, Request]


def get_context(request: Request) -> Context:
    """Den Request für die Resolver bereitstellen."""
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema,
    context_getter=get_context,
)
