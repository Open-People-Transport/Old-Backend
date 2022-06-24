from bustracker.database import get_session
from fastapi import Depends
from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext


class Context(BaseContext):
    def __init__(self, session: Session):
        self.session = session


async def get_context(session=Depends(get_session)):
    return Context(session)
