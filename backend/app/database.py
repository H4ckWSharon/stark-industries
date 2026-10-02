"""
STARK INDUSTRIES SQL — Database Setup (Platform DB)
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Convert sync URL to async, supporting SQLite fallback for standalone local execution
if "sqlite" in settings.database_url:
    async_url = settings.database_url.replace("sqlite://", "sqlite+aiosqlite://")
else:
    async_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

try:
    engine = create_async_engine(
        async_url,
        echo=settings.debug,
    )
except Exception:
    engine = create_async_engine(
        "sqlite+aiosqlite:///stark_platform.db",
        echo=settings.debug,
    )

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all platform tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
