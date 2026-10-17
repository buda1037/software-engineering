"""Configure the TLS certificate and private key resources."""

from importlib.resources import files
from typing import Final

from student.config.config import app_config, resources_path

__all__ = ["tls_certfile", "tls_keyfile"]

_tls_toml: Final = app_config.get("tls", {})
_tls_path = files(resources_path).joinpath("tls")

_key: Final[str] = _tls_toml.get("key", "key.pem")
_certificate: Final[str] = _tls_toml.get("certificate", "certificate.crt")

tls_keyfile = _tls_path.joinpath(_key)
tls_certfile = _tls_path.joinpath(_certificate)
