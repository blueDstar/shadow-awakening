import json
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, DailyQuest, QuestHistory, Character, ExperienceLog, Streak
from app.services.quest_engine import generate_daily_quests
from app.services.stat_service import update_stats
from app.services.streak_service import update_streak
from app.utils.exp_calculator import check_level_up

router = APIRouter(prefix="/api/quests", tags=["quests"])


@router.get("/today")
async def get_today_quests(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get or generate today's quests."""
    quests = await generate_daily_quests(db, user)
    
    total = len(quests)
    completed = sum(1 for q in quests if q.status == "completed")
    failed = sum(1 for q in quests if q.status == "failed")
    
    return {
        "quests": [
            {
                "id": str(q.id),
                "title_vi": q.title_vi,
                "title_en": q.title_en,
                "description_vi": q.description_vi,
                "description_en": q.description_en,
                "quest_type": q.quest_type,
                "category": q.category,
                "difficulty": q.difficulty,
                "exp_reward": q.exp_reward,
                "stat_rewards": q.stat_rewards,
                "status": q.status,
                "quest_date": str(q.quest_date),
                "completed_at": q.completed_at.isoformat() if q.completed_at else None,
                "fail_reason": q.fail_reason,
            }
            for q in quests
        ],
        "total": total,
        "completed": completed,
        "failed": failed,
        "day_completed": completed == total and total > 0,
        "quest_date": str(date.today()),
    }


@router.post("/{quest_id}/complete")
async def complete_quest(
    quest_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a quest as completed and award EXP + stats."""
    result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.id == quest_id, DailyQuest.user_id == user.id)
        )
    )
    quest = result.scalar_one_or_none()
    
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    if quest.status == "completed":
        raise HTTPException(status_code=400, detail="Quest already completed")
    
    # Mark complete
    quest.status = "completed"
    quest.completed_at = datetime.utcnow()
    
    # Award EXP
    char_result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = char_result.scalar_one_or_none()
    
    leveled_up = False
    new_level = character.level if character else 1
    
    if character:
        character.current_exp += quest.exp_reward
        character.total_exp += quest.exp_reward
        
        # Check level up
        new_level, remaining_exp, leveled_up = check_level_up(character.level, character.current_exp)
        if leveled_up:
            character.level = new_level
            character.current_exp = remaining_exp
        
        # Log EXP
        exp_log = ExperienceLog(
            user_id=user.id,
            amount=quest.exp_reward,
            source="quest",
            source_id=str(quest.id),
        )
        db.add(exp_log)
    
    # Award stats
    stat_rewards = json.loads(quest.stat_rewards) if quest.stat_rewards else {}
    if stat_rewards:
        # Get overall streak for bonus
        streak_result = await db.execute(
            select(Streak).where(
                and_(Streak.user_id == user.id, Streak.streak_type == "overall")
            )
        )
        overall = streak_result.scalar_one_or_none()
        streak_bonus = 1 + min((overall.current_streak if overall else 0) * 0.02, 0.5)
        await update_stats(db, user.id, stat_rewards, streak_bonus)
    
    # Update category streak
    category_to_streak = {
        "wisdom": "reading",
        "fitness": "fitness",
        "focus": "deep_work",
        "discipline": "journal",
        "exploration": "research",
        "confidence": "overall",
    }
    streak_type = category_to_streak.get(quest.category, "overall")
    await update_streak(db, user.id, streak_type)
    
    # Check if all quests completed today
    all_quests_result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user.id, DailyQuest.quest_date == date.today())
        )
    )
    all_quests = all_quests_result.scalars().all()
    all_completed = all(q.status == "completed" for q in all_quests)
    
    if all_completed:
        await update_streak(db, user.id, "overall")
    
    await db.flush()
    
    return {
        "status": "completed",
        "exp_earned": quest.exp_reward,
        "stat_rewards": stat_rewards,
        "leveled_up": leveled_up,
        "new_level": new_level,
        "day_completed": all_completed,
    }


@router.post("/{quest_id}/fail")
async def fail_quest(
    quest_id: str,
    fail_reason: str = "forgot",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a quest as failed."""
    result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.id == quest_id, DailyQuest.user_id == user.id)
        )
    )
    quest = result.scalar_one_or_none()
    
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    
    quest.status = "failed"
    quest.fail_reason = fail_reason
    await db.flush()
    
    return {"status": "failed", "fail_reason": fail_reason}


@router.get("/history")
async def get_quest_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 30,
):
    """Get quest history."""
    result = await db.execute(
        select(QuestHistory)
        .where(QuestHistory.user_id == user.id)
        .order_by(QuestHistory.quest_date.desc())
        .limit(limit)
    )
    histories = result.scalars().all()
    
    return [
        {
            "quest_date": str(h.quest_date),
            "total_quests": h.total_quests,
            "completed_quests": h.completed_quests,
            "failed_quests": h.failed_quests,
            "exp_earned": h.exp_earned,
            "day_completed": h.day_completed,
        }
        for h in histories
    ]
