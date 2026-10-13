"""ASGI server that runs the student REST service."""

from os import environ
from typing import Final

import uvicorn

from student.fastapi_app import app

__all__ = ["run"]


def run() -> None:
    """Start the student REST service."""
    uvicorn.run(app, host="127.0.0.1", port=8000)
