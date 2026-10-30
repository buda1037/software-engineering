"""Router für die HTTP-Endpunkte des Student-Service."""

from student.router.hello_router import router as hello_router
from student.router.student_router import student_router
from student.router.student_write_router import student_write_router

__all__ = ["hello_router", "student_router", "student_write_router"]
