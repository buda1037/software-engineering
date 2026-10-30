"""Router für Tokens von Keycloak."""

from json import JSONDecodeError
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from loguru import logger

from student.security.dependencies import get_token_service
from student.security.exceptions import LoginError
lazy from student.security.token_service import TokenService

__all__ = ["auth_router"]


auth_router: Final = APIRouter(tags=["Login"])


async def request_body_to_dict(request: Request) -> dict[str, Any]:
    """Den Request-Body ohne Pydantic lesen, damit Fehler 401 statt 422 liefern."""
    try:
        body: Final = await request.json()
    except JSONDecodeError:
        return {}
    return body if isinstance(body, dict) else {}


@auth_router.post("/token")
def token(
    body: Annotated[dict[str, Any], Depends(request_body_to_dict)],
    service: Annotated[TokenService, Depends(get_token_service)],
) -> JSONResponse:
    """POST-Request mit Benutzername und Passwort, um einen Access Token zu erhalten.

    :param body: Request-Body mit username und password
    :param service: Injizierter Service für Tokens
    :return: Response mit Token, Ablaufzeit in Sekunden und Rollen
    :rtype: JSONResponse
    :raises LoginError: Falls Benutzername oder Passwort fehlt oder falsch ist
    """
    username: Final = body.get("username")
    password: Final = body.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        raise LoginError(username=str(username))

    token_response: Final = service.token(username=username, password=password)
    access_token: Final = token_response["access_token"]
    user: Final = service.get_user_from_token(token=access_token)
    logger.debug("user={}", user)
    return JSONResponse(
        content={
            "token": access_token,
            "expires_in": token_response["expires_in"],
            "roles": user.roles,
        },
    )
