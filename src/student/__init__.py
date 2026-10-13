"""Student REST service package."""

lazy from student.asgi_server import run
lazy from student.fastapi_app import app

__all__ = ["app", "run"]
