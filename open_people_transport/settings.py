from functools import lru_cache
from typing import TYPE_CHECKING

from pydantic import BaseSettings

if TYPE_CHECKING:
    PostgresDsn = str
else:
    from pydantic import PostgresDsn


class Settings(BaseSettings):
    postgres_url: PostgresDsn = (
        "postgresql://bustracker1:GnhkLL82@localhost:5432/bustracker_alpha"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
