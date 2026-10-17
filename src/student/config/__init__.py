"""Expose the server and TLS configuration."""

from student.config.server import host_binding, port
from student.config.tls import tls_certfile, tls_keyfile

__all__ = ["host_binding", "port", "tls_certfile", "tls_keyfile"]
