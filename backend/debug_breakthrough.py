import asyncio
from sqlalchemy import select
from app.db.database import SessionLocal
from app.models import User, Character, StatCap, DailyQuest
from datetime import date

async def test_quest_response():
    async with SessionLocal() as db:
        # Get first user
        result = await db.execute(select(User))
        user = result.scalars().first()
        if not user:
            print("No users found")
            return
            
        print(f"Testing for user: {user.username} ({user.id})")
        
        # Duplicate the _prepare_quest_response logic
        user_id = user.id
        quests = [] # empty for test
        target_date = date.today()
        
        char_result = await db.execute(select(Character).where(Character.user_id == user_id))
        character = char_result.scalar_one_or_none()
        if not character:
            print("No character found")
            return
            
        print(f"Character found: {character.name} ({character.id})")
        
        stat_cap = None
        cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
        stat_cap = cap_result.scalar_one_or_none()
        
        if stat_cap:
            print(f"StatCap found: breakthrough_available={stat_cap.breakthrough_available}")
        else:
            print("No StatCap found")

if __name__ == "__main__":
    asyncio.run(test_quest_response())
