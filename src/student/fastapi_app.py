"""Student REST service."""

from time import time
from typing import Final
lazy from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from starlette.routing import Route

from student.config.config import logger

__all__ = ["app"]

app: Final = FastAPI()


@app.middleware("http")
async def log_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Log one request summary without personal data."""
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


@app.get("/hello")
def hello() -> dict[str, str]:
    """Return hello world.

    :return: Hello world as dict
    """
    return {"Hello": "World"}
