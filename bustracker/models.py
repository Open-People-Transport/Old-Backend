from typing import Any

from sqlmodel import Field, Relationship

from .database import BaseModel


def example(value: Any) -> dict[str, Any]:
    return {"example": value}


class Type(BaseModel, table=True):
    """
    A type of public transportation (e.g. bus, train, etc.).
    """

    name: str = Field(
        description="The name of the type, in lowercase",
        primary_key=True,
        max_length=12,
        schema_extra=example("bus"),
    )
