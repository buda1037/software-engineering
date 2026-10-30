"""Konfiguration für python-keycloak zum Zugriff auf Keycloak."""

from dataclasses import dataclass
from os import environ
from typing import Final

from dotenv import load_dotenv
from loguru import logger

from student.config.config import app_config

__all__ = ["KeycloakConfig", "keycloak_config"]


@dataclass(frozen=True, eq=False, slots=True, kw_only=True)
class KeycloakConfig:
    """Konfigurationsdaten für Keycloak."""

    server_url: str
    realm_name: str
    client_id: str
    client_secret_key: str


_keycloak_toml: Final = app_config.get("keycloak", {})
_schema: Final[str] = _keycloak_toml.get("schema", "http")
_host: Final[str] = _keycloak_toml.get("host", "localhost")
_port: Final[int] = _keycloak_toml.get("port", 8880)

# Das Client-Geheimnis steht in der Umgebungsvariablen KEYCLOAK_CLIENT_SECRET,
# lokal in der Datei .env im Hauptverzeichnis.
load_dotenv()

keycloak_config: Final = KeycloakConfig(
    server_url=f"{_schema}://{_host}:{_port}/",
    realm_name=_keycloak_toml.get("realm", "student"),
    client_id=_keycloak_toml.get("client-id", "student-client"),
    client_secret_key=environ.get("KEYCLOAK_CLIENT_SECRET", ""),
)
"""Zugriff auf Keycloak durch python-keycloak."""

if not keycloak_config.client_secret_key:
    logger.warning("keycloak: KEYCLOAK_CLIENT_SECRET ist nicht gesetzt")
logger.debug(
    "keycloak: server_url={}, realm_name={}, client_id={}",
    keycloak_config.server_url,
    keycloak_config.realm_name,
    keycloak_config.client_id,
)
