from typing import Any
from uuid import UUID, uuid4

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


class Route(BaseModel, table=True):
    """
    A transport route that passes through multiple stops
    and has vehicles going along itself.
    """

    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    number: str = Field(max_length=6, schema_extra=example("1"))
    type_name: str = Field(foreign_key=Type.name)
    type: Type = Relationship()
