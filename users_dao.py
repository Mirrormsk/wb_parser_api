from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from models import User
from config import settings

engine = create_async_engine(settings.DB_URL, echo=True)


class UsersDao:
    """Data access object for users table"""

    engine = engine

    @classmethod
    async def get_user_by_phone(cls, phone: str) -> User:
        """Get user by phone"""
        async with AsyncSession(cls.engine) as session:
            query = select(User).where(User.phone == phone)
            result = await session.exec(query)
            return result.one_or_none()

    @classmethod
    async def create_user(cls, phone: str) -> User:
        """Create new user"""
        user = User(phone=phone)

        async with AsyncSession(cls.engine) as session:
            session.add(user)
            await session.commit()

        return user

    @classmethod
    async def get_user_by_phone_or_create(
        cls, session: AsyncSession, phone: str
    ) -> User:
        """Retrieve user by phone if existed, else create"""
        query = select(User).where(User.phone == phone)
        results = await session.exec(query)

        if results:
            user = results.first()
            return user

        user = User(phone=phone)
        session.add(user)
        await session.commit()
        return user


def create_db_and_tables():
    engine = create_engine(settings.DB_CREATE_URL)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
