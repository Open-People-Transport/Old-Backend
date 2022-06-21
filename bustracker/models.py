from typing import Any

from sqlmodel import Field, Relationship

from .database import BaseModel


def example(value: Any) -> dict[str, Any]:
    return {"example": value}


class City(BaseModel, table=True):
    abbr: str = Field(primary_key=True, max_length=16, schema_extra=example("es"))
    name: str = Field(max_length=32, schema_extra=example("Example City"))
