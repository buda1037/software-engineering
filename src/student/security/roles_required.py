"""Überprüfung der erforderlichen Rollen."""

from typing import Annotated, Final

from fastapi import Depends, HTTPException, Request, status
from loguru import logger

from student.security.dependencies import get_token_service
lazy from student.security.role import Role
lazy from student.security.token_service import TokenService
lazy from student.security.user import User

__all__ = ["RolesRequired"]


class RolesRequired:
    """Dependency, die eine der erforderlichen Rollen prüft."""

    def __init__(self, *required_roles: Role) -> None:
        """Initialisierung mit den erforderlichen Rollen.

        :param required_roles: Rollen, von denen der Benutzer mindestens eine braucht
        """
        self.required_roles: Final = required_roles

    def __call__(
        self,
        request: Request,
        service: Annotated[TokenService, Depends(get_token_service)],
    ) -> User:
        """Den Benutzer aus dem Token ermitteln und seine Rollen prüfen.

        :param request: Request mit dem Header Authorization
        :param service: Injizierter Service für Tokens
        :return: Der Benutzer aus dem Token
        :rtype: User
        :raises HTTPException: 403, falls dem Benutzer die Rollen fehlen
        """
        user: Final = service.get_user_from_request(request)
        if not any(role in user.roles for role in self.required_roles):
            logger.debug("{} hat keine der Rollen {}", user, self.required_roles)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return user
