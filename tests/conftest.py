import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.db.core import Base
from src.main import app
from src.dependencies import get_db
from src.rate_limiting import limiter


# In-memory SQLite URL for async
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create engine and session factory for tests
test_engine = create_async_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Create tables in in-memory DB
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    # Drop tables after test (optional with in-memory SQLite)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    # Override the DB dependency
    async def override_get_db():
        yield db_session

    # Reset rate limiter if you're using `slowapi` or similar
    limiter.reset()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
