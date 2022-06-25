from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Type

from bustracker import api


@dataclass
class ResourceException(Exception):
    type: Type[api.BaseModel]
    identifier: Any
    detail: Optional[Any] = None


class ResourceNotFound(ResourceException):
    pass


class ResourceAlreadyExists(ResourceException):
    pass


class DatabaseConstraintsViolated(ResourceException):
    pass
