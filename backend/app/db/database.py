from importlib import import_module
from typing import Iterable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.database_url_async,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    connect_args=settings.database_connect_args,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


MODEL_MODULES: Iterable[str] = (
    "app.models.user",
    "app.models.character",
    "app.models.quest",
    "app.models.reward",
    "app.models.skill",
    "app.models.streak",
    "app.models.breakthrough",
    "app.models.challenge",
    "app.models.journal",
    "app.models.planner",
    "app.models.stat",
)


def load_model_metadata() -> None:
    """Import all model modules so Base.metadata knows every table."""
    for module_path in MODEL_MODULES:
        import_module(module_path)


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def sync_database_schema() -> None:
    """Automatically add missing columns to reduce production crashes."""
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS avatar_url VARCHAR"))
            await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS cover_url VARCHAR"))
            await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS background_url VARCHAR"))
            print("🌑 Database schema synchronized successfully.")
        except Exception as exc:
            print(f"🌑 Database sync warning: {exc}")


async def init_db() -> None:
    """Load models, create tables, then apply lightweight schema sync."""
    load_model_metadata()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await sync_database_schema()


__all__ = [
    "Base",
    "engine",
    "async_session",
    "get_db",
    "init_db",
    "sync_database_schema",
    "load_model_metadata",
]
