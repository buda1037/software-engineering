"""Filter für die Studentensuche."""

from dataclasses import dataclass

lazy from student.entity import StudyProgram

__all__ = ["StudentSuchparameter"]


@dataclass(frozen=True, slots=True, kw_only=True)
class StudentSuchparameter:
    """Suchparameter für die Studentensuche."""

    email: str | None = None
    """Exakte Emailadresse als Suchparameter."""

    last_name: str | None = None
    """Teil des Nachnamens als Suchparameter."""

    study_program: StudyProgram | None = None
    """Studiengang als Suchparameter."""

    def is_empty(self) -> bool:
        """Prüft, ob kein Suchparameter gesetzt ist."""
        return (
            self.email is None and self.last_name is None and self.study_program is None
        )
