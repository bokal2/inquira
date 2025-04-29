from sqlalchemy.ext.asyncio import AsyncSession
from src.db.core import async_session


async def get_db() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session
