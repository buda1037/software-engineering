"""Tokens von Keycloak anfordern und prüfen."""

from typing import Any, Final
lazy from collections.abc import Mapping

from jwcrypto.common import JWException
from keycloak import KeycloakAuthenticationError, KeycloakOpenID, KeycloakPostError
from loguru import logger
lazy from fastapi import Request

from student.config.keycloak import keycloak_config
from student.security.exceptions import AuthorizationError, LoginError
from student.security.role import Role
from student.security.user import User

__all__ = ["TokenService"]


class TokenService:
    """Schnittstelle zu Keycloak für Tokens."""

    def __init__(self) -> None:
        """Initialisierung der Schnittstelle zu Keycloak."""
        self.keycloak = KeycloakOpenID(
            server_url=keycloak_config.server_url,
            realm_name=keycloak_config.realm_name,
            client_id=keycloak_config.client_id,
            client_secret_key=keycloak_config.client_secret_key,
        )

    def token(self, username: str, password: str) -> dict[str, Any]:
        """Zu Benutzername und Passwort einen Access Token von Keycloak anfordern.

        :param username: Benutzername
        :param password: Passwort
        :return: Antwort von Keycloak mit Access Token und Ablaufzeit
        :rtype: dict[str, Any]
        :raises LoginError: Falls Benutzername oder Passwort falsch ist
        """
        logger.debug("username={}", username)
        try:
            return self.keycloak.token(username=username, password=password)
        except (KeycloakAuthenticationError, KeycloakPostError) as err:
            logger.debug("err={}", err)
            raise LoginError(username=username) from err

    def get_user_from_request(self, request: Request) -> User:
        """Die Benutzerdaten aus dem Header Authorization extrahieren.

        :param request: Request mit dem Header "Authorization: Bearer <Token>"
        :return: Benutzername und Rollen
        :rtype: User
        :raises AuthorizationError: Falls der Header fehlt oder der Token ungültig ist
        """
        authorization: Final = request.headers.get("Authorization")
        if authorization is None:
            raise AuthorizationError
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise AuthorizationError
        return self.get_user_from_token(token=token)

    def get_user_from_token(self, token: str) -> User:
        """Die Benutzerdaten aus einem Access Token extrahieren.

        :param token: Access Token von Keycloak
        :return: Benutzername und Rollen
        :rtype: User
        :raises AuthorizationError: Falls der Token ungültig oder abgelaufen ist
        """
        try:
            claims: Final = self.keycloak.decode_token(token=token)
            user: Final = User(
                username=claims["preferred_username"],
                roles=self._get_roles(claims),
            )
        except (JWException, KeyError, TypeError, ValueError) as err:
            logger.debug("err={}", err)
            raise AuthorizationError from err

        logger.debug("user={}", user)
        return user

    def _get_roles(self, claims: Mapping[str, Any]) -> list[Role]:
        """Die Rollen des Clients aus den Claims eines Tokens extrahieren."""
        client_access: Final = claims.get("resource_access", {}).get(
            self.keycloak.client_id,
            {},
        )
        return [Role(role) for role in client_access.get("roles", []) if role in Role]
