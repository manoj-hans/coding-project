from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.models import User
from fastapi import Depends

from calendly.db.dependencies import get_db_session

class UserDAO:
    """Data Access Object for User model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(self, name: str, email: str) -> User:
        # Check if the email is already in use
        existing_user = await self.session.execute(
            select(User).where(User.email == email)
        )
        if existing_user.scalars().first() is not None:
            raise ValueError(
                f"The email {email} is already in use. Please use a different email.")

        user = User(name=name, email=email)
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as ie:
            await self.session.rollback()
            raise ValueError(f"Failed to create user due to integrity error: {ie}")
        except Exception as ex:
            await self.session.rollback()
            raise Exception(f"An error occurred: {ex}")

        return user
