"""Exceptions für die Geschäftslogik."""

lazy from student.repository.student_suchparameter import StudentSuchparameter


class AddressRequiredError(RuntimeError):
    """Exception, falls eine Adresse im aktuellen Zustand None ist."""

    def __init__(self) -> None:
        """Initialisierung von AddressRequiredError."""
        super().__init__("Ungueltiger Zustand: Adresse ist None")


class EmailExistsError(Exception):
    """Exception, falls die Emailadresse bereits verwendet wird."""

    def __init__(self, email: str) -> None:
        """Initialisierung mit der bereits verwendeten Emailadresse."""
        super().__init__(f"Die Emailadresse {email} existiert bereits")
        self.email = email


class MatriculationNumberExistsError(Exception):
    """Exception, falls die Matrikelnummer bereits verwendet wird."""

    def __init__(self, matriculation_number: str) -> None:
        """Initialisierung mit der bereits verwendeten Matrikelnummer."""
        super().__init__(
            f"Die Matrikelnummer {matriculation_number} existiert bereits",
        )
        self.matriculation_number = matriculation_number


class UsernameExistsError(Exception):
    """Exception, falls der Benutzername bereits verwendet wird."""

    def __init__(self, username: str) -> None:
        """Initialisierung mit dem bereits verwendeten Benutzernamen."""
        super().__init__(f"Der Benutzername {username} existiert bereits")
        self.username = username


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
