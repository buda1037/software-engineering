"""Factory-Funktion für Dependency Injection."""

from student.security.token_service import TokenService

__all__ = ["get_token_service"]

_token_service = TokenService()


def get_token_service() -> TokenService:
    """Factory-Funktion für TokenService als Singleton."""
    return _token_service
