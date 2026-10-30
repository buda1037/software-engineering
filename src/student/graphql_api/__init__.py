"""GraphQL-Schnittstelle."""

from student.graphql_api.graphql_types import (
    AddressInput,
    CreatePayload,
    ExamResultInput,
    SearchParameters,
    StudentInput,
)
from student.graphql_api.schema import Mutation, Query, graphql_router

__all__ = [
    "AddressInput",
    "CreatePayload",
    "ExamResultInput",
    "Mutation",
    "Query",
    "SearchParameters",
    "StudentInput",
    "graphql_router",
]
