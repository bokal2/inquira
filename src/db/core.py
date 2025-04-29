import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging
from urllib.parse import quote_plus
from src.config import settings

logger = logging.getLogger(__name__)

# URL-encode password to handle special characters
ENCODED_PASSWORD = quote_plus(settings.db_password)

database_url = f"postgresql+asyncpg://{settings.db_user}:{ENCODED_PASSWORD}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# Create async engine
engine = create_async_engine(database_url, echo=True)

Base = declarative_base()

# Create async session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
