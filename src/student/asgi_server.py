"""ASGI server that runs the student REST service."""

from importlib.resources import as_file, files
from os import environ

import uvicorn

from student.fastapi_app import app

__all__ = ["run"]


def run() -> None:
    """Start the student REST service over HTTPS."""
    tls_resources = files("student").joinpath("config", "resources", "tls")

    with (
        as_file(tls_resources.joinpath("certificate.crt")) as certificate_path,
        as_file(tls_resources.joinpath("key.pem")) as key_path,
    ):
        uvicorn.run(
            app,
            host=environ.get("UVICORN_HOST", "127.0.0.1"),
            port=8000,
            ssl_certfile=str(certificate_path),
            ssl_keyfile=str(key_path),
        )
