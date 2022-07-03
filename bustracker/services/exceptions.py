from dataclasses import dataclass
from typing import Any, ClassVar, Type

from bustracker.core.models import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT


@dataclass
class ResourceException(Exception):
    """Unknown resource error"""

    status_code: ClassVar[int] = HTTP_400_BAD_REQUEST

    def asdict(self) -> dict:
        return {
            "description": self.__doc__,
        }


@dataclass
class ResourceNotFound(ResourceException):
    """Resource with given identity could not be found"""

    status_code: ClassVar[int] = HTTP_404_NOT_FOUND
    resource_type: Type[BaseModel]
    resource_identifier: Any

    def asdict(self) -> dict:
        return {
            "description": self.__doc__,
            "resource_type": self.resource_type.__name__,
            "resource_identifier": str(self.resource_identifier),
        }


@dataclass
class ResourceAlreadyExists(ResourceException):
    """Resource with given identity already exists"""

    status_code: ClassVar[int] = HTTP_409_CONFLICT
    resource_type: Type[BaseModel]
    resource_identifier: Any

    def asdict(self) -> dict:
        return {
            "description": self.__doc__,
            "resource_type": self.resource_type.__name__,
            "resource_identifier": str(self.resource_identifier),
        }


@dataclass
class DatabaseIntegrityViolated(ResourceException):
    """Operation violates database integrity"""

    status_code: ClassVar[int] = HTTP_409_CONFLICT
    resource_type: Type[BaseModel]
    details: Any

    def asdict(self) -> dict:
        return {
            "description": self.__doc__,
            "resource_type": self.resource_type.__name__,
            "details": str(self.details),
        }
