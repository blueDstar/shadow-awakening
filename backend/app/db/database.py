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
        print("🌑 Starting database schema synchronization...")
        
        columns_to_add = [
            ("characters", "avatar_url", "VARCHAR"),
            ("characters", "cover_url", "VARCHAR"),
            ("characters", "background_url", "VARCHAR"),
        ]

        for table, column, col_type in columns_to_add:
            try:
                # PostgreSQL specific check for column existence before adding
                # ADD COLUMN IF NOT EXISTS is cleaner but let's be super explicit
                await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {col_type}"))
                print(f"🌑 Column '{column}' checked/added to table '{table}'.")
            except Exception as e:
                print(f"🌑 Warning sync column '{column}': {e}")
        
        print("🌑 Database schema synchronization completed.")


async def init_db():
    # Create missing tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Sync columns
    await sync_database_schema()
