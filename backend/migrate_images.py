import asyncio
from app.db.database import engine
from sqlalchemy import text

async def migrate():
    async with engine.begin() as conn:
        print("Migrating characters table...")
        await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS avatar_url TEXT"))
        await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS cover_url TEXT"))
        await conn.execute(text("ALTER TABLE characters ADD COLUMN IF NOT EXISTS background_url TEXT"))
        print("Migration complete!")

if __name__ == "__main__":
    asyncio.run(migrate())
