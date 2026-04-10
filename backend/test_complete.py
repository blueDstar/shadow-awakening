import asyncio
from sqlalchemy import select
from app.db.database import async_session
from app.routes.quests import complete_quest
from app.models import DailyQuest, User

async def main():
    async with async_session() as db:
        # Get first user
        result = await db.execute(select(User))
        user = result.scalars().first()
        if not user:
            print("No user")
            return
            
        print("Test with user:", user.email)
        
        # Get first pending quest
        q_res = await db.execute(select(DailyQuest).where(DailyQuest.user_id == user.id, DailyQuest.status == "pending"))
        quest = q_res.scalars().first()
        if not quest:
            print("No pending quest, generating today quests")
            from app.services.quest_engine import generate_daily_quests
            from datetime import date
            quests = await generate_daily_quests(db, user, date.today())
            quest = quests[0]
            await db.commit()
            
        print("Completing quest:", quest.id)
        try:
            res = await complete_quest(str(quest.id), user, db)
            print("Success:", res)
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
