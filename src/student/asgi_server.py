"""ASGI server that runs the student REST service."""

from importlib.resources import as_file

import uvicorn

from student.config import host_binding, port, tls_certfile, tls_keyfile
from student.fastapi_app import app

__all__ = ["run"]


def run() -> None:
    """Start the student REST service over HTTPS."""
    with (
        as_file(tls_certfile) as certificate_path,
        as_file(tls_keyfile) as key_path,
    ):
        uvicorn.run(
            app,
            host=host_binding,
            port=port,
            ssl_certfile=str(certificate_path),
            ssl_keyfile=str(key_path),
        )
