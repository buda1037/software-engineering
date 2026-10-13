"""ASGI server that runs the student REST service."""

from os import environ

import uvicorn

from student.fastapi_app import app

__all__ = ["run"]


def run() -> None:
    """Start the student REST service."""
    uvicorn.run(app, host=environ.get("UVICORN_HOST", "127.0.0.1"), port=8000)
