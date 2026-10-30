"""Student REST service."""

from time import time
from typing import Final
lazy from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.routing import Route

from student.config.config import logger
from student.graphql_api import graphql_router
from student.router import hello_router, student_router, student_write_router
from student.security import AuthorizationError, LoginError, auth_router

__all__ = ["app"]


app: Final = FastAPI()


@app.middleware("http")
async def log_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Protokolliert eine Anfrage mit Status und Dauer."""
    start = time()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration_ms = (time() - start) * 1000
        route = request.scope.get("route")
        route_path = route.path if isinstance(route, Route) else "<unmatched>"

        logger.info(
            "HTTP {} {} status={} duration_ms={:.2f}",
            request.method,
            route_path,
            status_code,
            duration_ms,
        )


# --------------------------------------------------------------------------------------
# R E S T
# --------------------------------------------------------------------------------------
app.include_router(student_router, prefix="/rest")
app.include_router(hello_router, prefix="/hello")
app.include_router(student_write_router, prefix="/rest")
app.include_router(auth_router, prefix="/auth")


# --------------------------------------------------------------------------------------
# G r a p h Q L
# --------------------------------------------------------------------------------------
app.include_router(graphql_router, prefix="/graphql")


# --------------------------------------------------------------------------------------
# S e c u r i t y
# --------------------------------------------------------------------------------------
@app.exception_handler(AuthorizationError)
def authorization_error_handler(
    _request: Request,
    _err: AuthorizationError,
) -> Response:
    """Fehlender oder ungültiger Token.

    :return: Response mit Statuscode 401
    :rtype: Response
    """
    return Response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(LoginError)
def login_error_handler(_request: Request, err: LoginError) -> Response:
    """Fehlerhafter Benutzername oder fehlerhaftes Passwort.

    :return: Response mit Statuscode 401
    :rtype: Response
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(err)},
    )
