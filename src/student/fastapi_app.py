"""Student REST service."""

from time import time
from typing import Final
lazy from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from starlette.routing import Route

from student.config.config import logger
from student.router import hello_router, student_router

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
