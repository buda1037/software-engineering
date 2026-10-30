"""Entity-Klassen der Anwendung."""

from student.entity.address import Address
from student.entity.base import Base
from student.entity.exam_result import ExamResult
from student.entity.gender import Gender
from student.entity.student import Student
from student.entity.study_program import StudyProgram

__all__ = [
    "Address",
    "Base",
    "ExamResult",
    "Gender",
    "Student",
    "StudyProgram",
]
