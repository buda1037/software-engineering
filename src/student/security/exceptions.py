"""Exceptions beim Zugriffsschutz."""

__all__ = ["AuthorizationError", "LoginError"]


class LoginError(Exception):
    """Exception, falls Benutzername oder Passwort fehlerhaft ist."""

    def __init__(self, username: str | None = None) -> None:
        """Initialisierung mit dem Benutzernamen.

        :param username: Benutzername
        """
        super().__init__(f"Fehlerhafte Benutzerdaten fuer {username}")
        self.username = username


class AuthorizationError(Exception):
    """Exception, falls der Token fehlt oder ungültig ist."""
