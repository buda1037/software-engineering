"""Configure the ASGI server host and port."""

from typing import Final

from student.config.config import app_config

__all__ = ["host_binding", "port"]

_server_toml: Final = app_config.get("server", {})

host_binding: Final[str] = _server_toml.get("host-binding", "127.0.0.1")
port: Final[int] = _server_toml.get("port", 8000)
