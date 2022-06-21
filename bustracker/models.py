from typing import Any

from sqlmodel import Field, Relationship

from .database import BaseModel


def example(value: Any) -> dict[str, Any]:
    return {"example": value}
