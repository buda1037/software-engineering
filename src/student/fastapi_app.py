"""Student REST service."""

from typing import Final

from fastapi import FastAPI

__all__ = ["app"]

app: Final = FastAPI()


@app.get("/hello")
def hello() -> dict[str, str]:
    """Return hello world.

    :return: Hello world as dict
    """
    return {"Hello": "World"}
