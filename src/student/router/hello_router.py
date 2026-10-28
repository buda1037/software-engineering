"""HelloRouter."""

from typing import Final

from fastapi import APIRouter

__all__ = ["router"]


router: Final = APIRouter(tags=["Hello"])


@router.get("")
def hello() -> dict[str, str]:
    """Demo-Router für 'Hello World'.

    :return: JSON-Datensatz mit 'Hello World'
    :rtype: dict[str, str]
    """
    return {"Hello": "World"}
