"""Exceptions für die Geschäftslogik."""


class AddressRequiredError(RuntimeError):
    """Exception, falls eine Adresse im aktuellen Zustand None ist."""

    def __init__(self) -> None:
        """Initialisierung von AddressRequiredError."""
        super().__init__("Ungueltiger Zustand: Adresse ist None")


class NotFoundError(Exception):
    """Exception, falls kein Student gefunden wurde."""

    def __init__(self, student_id: int) -> None:
        """Initialisierung von NotFoundError mit der Student-ID.

        :param student_id: Student-ID, zu der nichts gefunden wurde
        """
        super().__init__("Not Found")
        self.student_id = student_id
