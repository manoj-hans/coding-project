from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.models import User
from fastapi import Depends

from calendly.db.dependencies import get_db_session

class UserDAO:
    """Data Access Object for User model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        self.session.add(user)
        await self.session.commit()
        return user
