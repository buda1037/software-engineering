"""Fixtures für Integrationstests gegen den laufenden Student-Server."""

from pathlib import Path
from ssl import create_default_context
lazy from collections.abc import Iterator

import httpx
import pytest


@pytest.fixture(scope="session")
def client() -> Iterator[httpx.Client]:
    """Stellt einen HTTP-Client mit dem lokalen Serverzertifikat bereit."""
    certificate = (
        Path(__file__).resolve().parents[2]
        / "src/student/config/resources/tls/certificate.crt"
    )
    tls_context = create_default_context(cafile=str(certificate))

    with httpx.Client(
        base_url="https://localhost:8000",
        verify=tls_context,
        timeout=10.0,
    ) as http_client:
        yield http_client
