from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


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


from sqlalchemy import text


async def sync_database_schema():
    """Automatically add missing columns to prevent crashes on production."""
    async with engine.begin() as conn:
        try:
            # Characters table: Add image URLs
            await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS avatar_url VARCHAR"))
            await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS cover_url VARCHAR"))
            await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS background_url VARCHAR"))
            
            # StatCaps table: Ensure it exists (create_all will do this, but just in case)
            # BreakthroughRituals table: ensure primary key is UUID
            
            print("🌑 Database schema synchronized successfully.")
        except Exception as e:
            print(f"🌑 Database sync warning: {e}")


async def init_db():
    # Create missing tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Sync columns
    await sync_database_schema()
