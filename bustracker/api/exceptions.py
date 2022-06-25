from __future__ import annotations

from typing import Any, Type

from bustracker import api


class ResourceNotFound(Exception):
    def __init__(
        self,
        type: Type[api.BaseModel],
        identifier: Any,
    ) -> None:
        self.type = type
        self.identifier = identifier
