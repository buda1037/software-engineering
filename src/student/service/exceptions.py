"""Exceptions für die Geschäftslogik."""

lazy from student.repository.student_suchparameter import StudentSuchparameter


class AddressRequiredError(RuntimeError):
    """Exception, falls eine Adresse im aktuellen Zustand None ist."""

    def __init__(self) -> None:
        """Initialisierung von AddressRequiredError."""
        super().__init__("Ungueltiger Zustand: Adresse ist None")


class NotFoundError(Exception):
    """Exception, falls kein Student gefunden wurde."""

    def __init__(
        self,
        student_id: int | None = None,
        *,
        suchparameter: StudentSuchparameter | None = None,
    ) -> None:
        """Initialisierung mit der Student-ID oder Suchparametern.

        :param student_id: Student-ID, zu der nichts gefunden wurde
        :param suchparameter: Suchparameter, zu denen nichts gefunden wurde
        """
        super().__init__("Not Found")
        self.student_id = student_id
        self.suchparameter = suchparameter
