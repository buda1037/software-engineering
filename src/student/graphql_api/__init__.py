"""GraphQL-Schnittstelle."""

from student.graphql_api.graphql_types import Suchparameter
from student.graphql_api.schema import Query, graphql_router

__all__ = ["Query", "Suchparameter", "graphql_router"]
